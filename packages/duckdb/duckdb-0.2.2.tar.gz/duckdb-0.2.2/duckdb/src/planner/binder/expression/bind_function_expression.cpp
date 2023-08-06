#include "duckdb/catalog/catalog.hpp"
#include "duckdb/catalog/catalog_entry/scalar_function_catalog_entry.hpp"
#include "duckdb/execution/expression_executor.hpp"
#include "duckdb/parser/expression/function_expression.hpp"
#include "duckdb/planner/expression/bound_cast_expression.hpp"
#include "duckdb/planner/expression/bound_constant_expression.hpp"
#include "duckdb/planner/expression/bound_function_expression.hpp"
#include "duckdb/planner/expression_binder.hpp"
#include "duckdb/planner/binder.hpp"

namespace duckdb {
using namespace std;

BindResult ExpressionBinder::BindExpression(FunctionExpression &function, idx_t depth) {
	// lookup the function in the catalog
	QueryErrorContext error_context(binder.root_statement, function.query_location);

	if (function.function_name == "unnest" || function.function_name == "unlist") {
		// special case, not in catalog
		// TODO make sure someone does not create such a function OR
		// have unnest live in catalog, too
		return BindUnnest(function, depth);
	}
	auto &catalog = Catalog::GetCatalog(context);
	auto func = catalog.GetEntry(context, CatalogType::SCALAR_FUNCTION_ENTRY, function.schema,
	                             function.function_name, false, error_context);
	if (func->type == CatalogType::SCALAR_FUNCTION_ENTRY) {
		// scalar function
		return BindFunction(function, (ScalarFunctionCatalogEntry *)func, depth);
	} else {
		// aggregate function
		return BindAggregate(function, (AggregateFunctionCatalogEntry *)func, depth);
	}
}

BindResult ExpressionBinder::BindFunction(FunctionExpression &function, ScalarFunctionCatalogEntry *func, idx_t depth) {
	// bind the children of the function expression
	string error;
	for (idx_t i = 0; i < function.children.size(); i++) {
		BindChild(function.children[i], depth, error);
	}
	if (!error.empty()) {
		return BindResult(error);
	}
	// all children bound successfully
	// extract the children and types
	vector<unique_ptr<Expression>> children;
	for (idx_t i = 0; i < function.children.size(); i++) {
		auto &child = (BoundExpression &)*function.children[i];
		children.push_back(move(child.expr));
	}
	// special binder-only functions
	// FIXME: these shouldn't be special
	if (function.function_name == "alias") {
		if (children.size() != 1) {
			throw BinderException(binder.FormatError(function, "alias function expects a single argument"));
		}
		// alias function: returns the alias of the current expression, or the name of the child
		string alias = !function.alias.empty() ? function.alias : children[0]->GetName();
		return BindResult(make_unique<BoundConstantExpression>(Value(alias)));
	} else if (function.function_name == "typeof") {
		if (children.size() != 1) {
			throw BinderException(binder.FormatError(function, "typeof function expects a single argument"));
		}
		// typeof function: returns the type of the child expression
		string type = children[0]->return_type.ToString();
		return BindResult(make_unique<BoundConstantExpression>(Value(type)));
	}
	auto result = ScalarFunction::BindScalarFunction(context, *func, move(children), error, function.is_operator);
	if (!result) {
		throw BinderException(binder.FormatError(function, error));
	}
	return BindResult(move(result));
}

BindResult ExpressionBinder::BindAggregate(FunctionExpression &expr, AggregateFunctionCatalogEntry *function,
                                           idx_t depth) {
	return BindResult(binder.FormatError(expr, UnsupportedAggregateMessage()));
}

BindResult ExpressionBinder::BindUnnest(FunctionExpression &expr, idx_t depth) {
	return BindResult(binder.FormatError(expr, UnsupportedUnnestMessage()));
}

string ExpressionBinder::UnsupportedAggregateMessage() {
	return "Aggregate functions are not supported here";
}

string ExpressionBinder::UnsupportedUnnestMessage() {
	return "UNNEST not supported here";
}

} // namespace duckdb
