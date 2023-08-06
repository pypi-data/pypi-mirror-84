#include "duckdb/parser/tableref/subqueryref.hpp"
#include "duckdb/planner/binder.hpp"
#include "duckdb/planner/tableref/bound_subqueryref.hpp"

namespace duckdb {
using namespace std;

unique_ptr<BoundTableRef> Binder::Bind(SubqueryRef &ref) {
	auto binder = make_unique<Binder>(context, this);
	binder->alias = ref.alias;
	for (auto &cte_it : ref.subquery->cte_map) {
		binder->AddCTE(cte_it.first, cte_it.second.get());
	}
	auto subquery = binder->BindNode(*ref.subquery->node);
	idx_t bind_index = subquery->GetRootIndex();
	auto result = make_unique<BoundSubqueryRef>(move(binder), move(subquery));

	bind_context.AddSubquery(bind_index, ref.alias, ref, *result->subquery);
	MoveCorrelatedExpressions(*result->binder);
	return move(result);
}

} // namespace duckdb
