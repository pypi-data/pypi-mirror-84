#include "duckdb/execution/operator/join/physical_comparison_join.hpp"
#include "duckdb/common/types/chunk_collection.hpp"

using namespace std;

namespace duckdb {

PhysicalComparisonJoin::PhysicalComparisonJoin(LogicalOperator &op, PhysicalOperatorType type,
                                               vector<JoinCondition> conditions_, JoinType join_type)
    : PhysicalJoin(op, type, join_type) {
	conditions.resize(conditions_.size());
	// we reorder conditions so the ones with COMPARE_EQUAL occur first
	idx_t equal_position = 0;
	idx_t other_position = conditions_.size() - 1;
	for (idx_t i = 0; i < conditions_.size(); i++) {
		if (conditions_[i].comparison == ExpressionType::COMPARE_EQUAL) {
			// COMPARE_EQUAL, move to the start
			conditions[equal_position++] = std::move(conditions_[i]);
		} else {
			// other expression, move to the end
			conditions[other_position--] = std::move(conditions_[i]);
		}
	}
}

string PhysicalComparisonJoin::ParamsToString() const {
	string extra_info = JoinTypeToString(join_type) + "\n";
	for (auto &it : conditions) {
		string op = ExpressionTypeToOperator(it.comparison);
		extra_info += it.left->GetName() + op + it.right->GetName() + "\n";
	}
	return extra_info;
}

void PhysicalComparisonJoin::ConstructEmptyJoinResult(JoinType join_type, bool has_null, DataChunk &input,
                                                      DataChunk &result) {
	// empty hash table, special case
	if (join_type == JoinType::ANTI) {
		// anti join with empty hash table, NOP join
		// return the input
		assert(input.column_count() == result.column_count());
		result.Reference(input);
	} else if (join_type == JoinType::MARK) {
		// MARK join with empty hash table
		assert(join_type == JoinType::MARK);
		assert(result.column_count() == input.column_count() + 1);
		auto &result_vector = result.data.back();
		assert(result_vector.type == LogicalType::BOOLEAN);
		// for every data vector, we just reference the child chunk
		result.SetCardinality(input);
		for (idx_t i = 0; i < input.column_count(); i++) {
			result.data[i].Reference(input.data[i]);
		}
		// for the MARK vector:
		// if the HT has no NULL values (i.e. empty result set), return a vector that has false for every input
		// entry if the HT has NULL values (i.e. result set had values, but all were NULL), return a vector that
		// has NULL for every input entry
		if (!has_null) {
			auto bool_result = FlatVector::GetData<bool>(result_vector);
			for (idx_t i = 0; i < result.size(); i++) {
				bool_result[i] = false;
			}
		} else {
			FlatVector::Nullmask(result_vector).set();
		}
	} else if (join_type == JoinType::LEFT || join_type == JoinType::OUTER || join_type == JoinType::SINGLE) {
		// LEFT/FULL OUTER/SINGLE join and build side is empty
		// for the LHS we reference the data
		result.SetCardinality(input.size());
		for (idx_t i = 0; i < input.column_count(); i++) {
			result.data[i].Reference(input.data[i]);
		}
		// for the RHS
		for (idx_t k = input.column_count(); k < result.column_count(); k++) {
			result.data[k].vector_type = VectorType::CONSTANT_VECTOR;
			ConstantVector::SetNull(result.data[k], true);
		}
	}
}

void PhysicalComparisonJoin::ConstructFullOuterJoinResult(bool *found_match, ChunkCollection &input, DataChunk &result,
                                                          idx_t &scan_position) {
	// fill in NULL values for the LHS
	SelectionVector rsel(STANDARD_VECTOR_SIZE);
	while (scan_position < input.count) {
		auto &rhs_chunk = *input.chunks[scan_position / STANDARD_VECTOR_SIZE];
		idx_t result_count = 0;
		// figure out which tuples didn't find a match in the RHS
		for (idx_t i = 0; i < rhs_chunk.size(); i++) {
			if (!found_match[scan_position + i]) {
				rsel.set_index(result_count++, i);
			}
		}
		scan_position += STANDARD_VECTOR_SIZE;
		if (result_count > 0) {
			// if there were any tuples that didn't find a match, output them
			idx_t left_column_count = result.column_count() - input.column_count();
			for (idx_t i = 0; i < left_column_count; i++) {
				result.data[i].vector_type = VectorType::CONSTANT_VECTOR;
				ConstantVector::SetNull(result.data[i], true);
			}
			for (idx_t col_idx = 0; col_idx < rhs_chunk.column_count(); col_idx++) {
				result.data[left_column_count + col_idx].Slice(rhs_chunk.data[col_idx], rsel, result_count);
			}
			result.SetCardinality(result_count);
			return;
		}
	}
}

} // namespace duckdb
