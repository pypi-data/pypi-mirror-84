#include "duckdb/execution/operator/scan/physical_table_scan.hpp"

#include <utility>

#include "duckdb/catalog/catalog_entry/table_catalog_entry.hpp"
#include "duckdb/transaction/transaction.hpp"
#include "duckdb/planner/expression/bound_conjunction_expression.hpp"

#include "duckdb/parallel/task_context.hpp"
#include "duckdb/common/string_util.hpp"

using namespace std;

namespace duckdb {

class PhysicalTableScanOperatorState : public PhysicalOperatorState {
public:
	PhysicalTableScanOperatorState(PhysicalOperator &op) : PhysicalOperatorState(op, nullptr), initialized(false) {
	}

	ParallelState *parallel_state;
	unique_ptr<FunctionOperatorData> operator_data;
	//! Whether or not the scan has been initialized
	bool initialized;
};

PhysicalTableScan::PhysicalTableScan(vector<LogicalType> types, TableFunction function_,
                                     unique_ptr<FunctionData> bind_data_p, vector<column_t> column_ids_p,
                                     vector<string> names_p, unordered_map<idx_t, vector<TableFilter>> table_filters_p)
    : PhysicalOperator(PhysicalOperatorType::TABLE_SCAN, move(types)), function(move(function_)),
      bind_data(move(bind_data_p)), column_ids(move(column_ids_p)), names(move(names_p)),
      table_filters(move(table_filters_p)) {
}

void PhysicalTableScan::GetChunkInternal(ExecutionContext &context, DataChunk &chunk, PhysicalOperatorState *state_) {
	auto &state = (PhysicalTableScanOperatorState &)*state_;
	if (column_ids.empty()) {
		return;
	}
	if (!state.initialized) {
		state.parallel_state = nullptr;
		if (function.init) {
			auto &task = context.task;
			// check if there is any parallel state to fetch
			state.parallel_state = nullptr;
			auto task_info = task.task_info.find(this);
			if (task_info != task.task_info.end()) {
				// parallel scan init
				state.parallel_state = task_info->second;
				state.operator_data = function.parallel_init(context.client, bind_data.get(), state.parallel_state,
				                                             column_ids, table_filters);
			} else {
				// sequential scan init
				state.operator_data = function.init(context.client, bind_data.get(), column_ids, table_filters);
			}
			if (!state.operator_data) {
				// no operator data returned: nothing to scan
				return;
			}
		}
		state.initialized = true;
	}
	if (!state.parallel_state) {
		// sequential scan
		function.function(context.client, bind_data.get(), state.operator_data.get(), chunk);
		if (chunk.size() != 0) {
			return;
		}
	} else {
		// parallel scan
		do {
			function.function(context.client, bind_data.get(), state.operator_data.get(), chunk);
			if (chunk.size() == 0) {
				assert(function.parallel_state_next);
				if (function.parallel_state_next(context.client, bind_data.get(), state.operator_data.get(),
				                                 state.parallel_state)) {
					continue;
				} else {
					break;
				}
			} else {
				return;
			}
		} while (true);
	}
	assert(chunk.size() == 0);
	if (function.cleanup) {
		function.cleanup(context.client, bind_data.get(), state.operator_data.get());
	}
}

string PhysicalTableScan::GetName() const {
	return StringUtil::Upper(function.name);
}

string PhysicalTableScan::ParamsToString() const {
	string result;
	if (function.to_string) {
		result = function.to_string(bind_data.get());
		result += "\n[INFOSEPARATOR]\n";
	}
	for (idx_t i = 0; i < column_ids.size(); i++) {
		if (column_ids[i] < names.size()) {
			if (i > 0) {
				result += "\n";
			}
			result += names[column_ids[i]];
		}
	}
	if (table_filters.size() > 0) {
		result += "\n[INFOSEPARATOR]\n";
		result += "Filters: ";
		for (auto &f : table_filters) {
			for (auto &filter : f.second) {
				if (filter.column_index < names.size()) {
					result += "\n";
					result += names[filter.column_index] + ExpressionTypeToOperator(filter.comparison_type) +
							filter.constant.ToString();
				}
			}
		}
	}
	return result;
}

unique_ptr<PhysicalOperatorState> PhysicalTableScan::GetOperatorState() {
	return make_unique<PhysicalTableScanOperatorState>(*this);
}

} // namespace duckdb
