#include "duckdb/optimizer/topn_optimizer.hpp"
#include "duckdb/planner/operator/logical_order.hpp"
#include "duckdb/planner/operator/logical_limit.hpp"
#include "duckdb/planner/operator/logical_top_n.hpp"
#include "duckdb/common/limits.hpp"

namespace duckdb {
using namespace std;

unique_ptr<LogicalOperator> TopN::Optimize(unique_ptr<LogicalOperator> op) {
	if (op->type == LogicalOperatorType::LIMIT && op->children[0]->type == LogicalOperatorType::ORDER_BY) {
		auto &limit = (LogicalLimit &)*op;
		auto &order_by = (LogicalOrder &)*(op->children[0]);

		// This optimization doesn't apply when OFFSET is present without LIMIT
		if (limit.limit != NumericLimits<int64_t>::Maximum()) {
			auto topn = make_unique<LogicalTopN>(move(order_by.orders), limit.limit, limit.offset);
			topn->AddChild(move(order_by.children[0]));
			op = move(topn);
		}
	} else {
		for (auto &child : op->children) {
			child = Optimize(move(child));
		}
	}
	return op;
}

} // namespace duckdb
