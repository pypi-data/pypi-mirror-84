#include "duckdb/planner/expression/bound_subquery_expression.hpp"

#include "duckdb/common/exception.hpp"

namespace duckdb {
using namespace std;

BoundSubqueryExpression::BoundSubqueryExpression(LogicalType return_type)
    : Expression(ExpressionType::SUBQUERY, ExpressionClass::BOUND_SUBQUERY, move(return_type)) {
}

string BoundSubqueryExpression::ToString() const {
	return "SUBQUERY";
}

bool BoundSubqueryExpression::Equals(const BaseExpression *other_) const {
	// equality between bound subqueries not implemented currently
	return false;
}

unique_ptr<Expression> BoundSubqueryExpression::Copy() {
	throw SerializationException("Cannot copy BoundSubqueryExpression");
}

} // namespace duckdb
