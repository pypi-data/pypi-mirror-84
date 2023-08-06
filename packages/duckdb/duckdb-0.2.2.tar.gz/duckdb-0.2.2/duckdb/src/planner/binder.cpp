#include "duckdb/planner/binder.hpp"

#include "duckdb/parser/statement/list.hpp"
#include "duckdb/planner/bound_query_node.hpp"
#include "duckdb/planner/bound_tableref.hpp"
#include "duckdb/planner/expression.hpp"

#include <algorithm>

namespace duckdb {
using namespace std;

Binder::Binder(ClientContext &context, Binder *parent_, bool inherit_ctes_)
    : context(context), read_only(true), parent(parent_), bound_tables(0), inherit_ctes(inherit_ctes_) {
	if (parent_ && inherit_ctes_) {
		// We have to inherit CTE bindings from the parent bind_context, if there is a parent.
		bind_context.SetCTEBindings(parent_->bind_context.GetCTEBindings());
		bind_context.cte_references = parent_->bind_context.cte_references;
		parameters = parent_->parameters;
	}
}

BoundStatement Binder::Bind(SQLStatement &statement) {
	root_statement = &statement;
	switch (statement.type) {
	case StatementType::SELECT_STATEMENT:
		return Bind((SelectStatement &)statement);
	case StatementType::INSERT_STATEMENT:
		return Bind((InsertStatement &)statement);
	case StatementType::COPY_STATEMENT:
		return Bind((CopyStatement &)statement);
	case StatementType::DELETE_STATEMENT:
		return Bind((DeleteStatement &)statement);
	case StatementType::UPDATE_STATEMENT:
		return Bind((UpdateStatement &)statement);
	case StatementType::RELATION_STATEMENT:
		return Bind((RelationStatement &)statement);
	case StatementType::CREATE_STATEMENT:
		return Bind((CreateStatement &)statement);
	case StatementType::DROP_STATEMENT:
		return Bind((DropStatement &)statement);
	case StatementType::ALTER_STATEMENT:
		return Bind((AlterStatement &)statement);
	case StatementType::TRANSACTION_STATEMENT:
		return Bind((TransactionStatement &)statement);
	case StatementType::PRAGMA_STATEMENT:
		return Bind((PragmaStatement &)statement);
	case StatementType::EXECUTE_STATEMENT:
		return Bind((ExecuteStatement &)statement);
	case StatementType::EXPLAIN_STATEMENT:
		return Bind((ExplainStatement &)statement);
	case StatementType::VACUUM_STATEMENT:
		return Bind((VacuumStatement &)statement);
	case StatementType::CALL_STATEMENT:
		return Bind((CallStatement &)statement);
	case StatementType::EXPORT_STATEMENT:
		return Bind((ExportStatement &)statement);
	default:
		throw NotImplementedException("Unimplemented statement type \"%s\" for Bind",
		                              StatementTypeToString(statement.type));
	}
}

unique_ptr<BoundQueryNode> Binder::BindNode(QueryNode &node) {
	unique_ptr<BoundQueryNode> result;
	switch (node.type) {
	case QueryNodeType::SELECT_NODE:
		result = BindNode((SelectNode &)node);
		break;
	case QueryNodeType::RECURSIVE_CTE_NODE:
		result = BindNode((RecursiveCTENode &)node);
		break;
	default:
		assert(node.type == QueryNodeType::SET_OPERATION_NODE);
		result = BindNode((SetOperationNode &)node);
		break;
	}
	return result;
}

BoundStatement Binder::Bind(QueryNode &node) {
	BoundStatement result;
	// bind the node
	auto bound_node = BindNode(node);

	result.names = bound_node->names;
	result.types = bound_node->types;

	// and plan it
	result.plan = CreatePlan(*bound_node);
	return result;
}

unique_ptr<LogicalOperator> Binder::CreatePlan(BoundQueryNode &node) {
	switch (node.type) {
	case QueryNodeType::SELECT_NODE:
		return CreatePlan((BoundSelectNode &)node);
	case QueryNodeType::SET_OPERATION_NODE:
		return CreatePlan((BoundSetOperationNode &)node);
	case QueryNodeType::RECURSIVE_CTE_NODE:
		return CreatePlan((BoundRecursiveCTENode &)node);
	default:
		throw Exception("Unsupported bound query node type");
	}
}
unique_ptr<BoundTableRef> Binder::Bind(TableRef &ref) {
	switch (ref.type) {
	case TableReferenceType::BASE_TABLE:
		return Bind((BaseTableRef &)ref);
	case TableReferenceType::CROSS_PRODUCT:
		return Bind((CrossProductRef &)ref);
	case TableReferenceType::JOIN:
		return Bind((JoinRef &)ref);
	case TableReferenceType::SUBQUERY:
		return Bind((SubqueryRef &)ref);
	case TableReferenceType::EMPTY:
		return Bind((EmptyTableRef &)ref);
	case TableReferenceType::TABLE_FUNCTION:
		return Bind((TableFunctionRef &)ref);
	case TableReferenceType::EXPRESSION_LIST:
		return Bind((ExpressionListRef &)ref);
	default:
		throw Exception("Unknown table ref type");
	}
}

unique_ptr<LogicalOperator> Binder::CreatePlan(BoundTableRef &ref) {
	switch (ref.type) {
	case TableReferenceType::BASE_TABLE:
		return CreatePlan((BoundBaseTableRef &)ref);
	case TableReferenceType::SUBQUERY:
		return CreatePlan((BoundSubqueryRef &)ref);
	case TableReferenceType::JOIN:
		return CreatePlan((BoundJoinRef &)ref);
	case TableReferenceType::CROSS_PRODUCT:
		return CreatePlan((BoundCrossProductRef &)ref);
	case TableReferenceType::TABLE_FUNCTION:
		return CreatePlan((BoundTableFunction &)ref);
	case TableReferenceType::EMPTY:
		return CreatePlan((BoundEmptyTableRef &)ref);
	case TableReferenceType::EXPRESSION_LIST:
		return CreatePlan((BoundExpressionListRef &)ref);
	case TableReferenceType::CTE:
		return CreatePlan((BoundCTERef &)ref);
	default:
		throw Exception("Unsupported bound table ref type type");
	}
}

void Binder::AddCTE(const string &name, CommonTableExpressionInfo *info) {
	assert(info);
	assert(!name.empty());
	auto entry = CTE_bindings.find(name);
	if (entry != CTE_bindings.end()) {
		throw BinderException("Duplicate CTE \"%s\" in query!", name);
	}
	CTE_bindings[name] = info;
}

CommonTableExpressionInfo *Binder::FindCTE(const string &name, bool skip) {
	auto entry = CTE_bindings.find(name);
	if (entry != CTE_bindings.end()) {
		if (!skip || entry->second->query->node->type == QueryNodeType::RECURSIVE_CTE_NODE) {
			return entry->second;
		}
	}
	if (parent && inherit_ctes) {
		return parent->FindCTE(name, name == alias);
	}
	return nullptr;
}

idx_t Binder::GenerateTableIndex() {
	if (parent) {
		return parent->GenerateTableIndex();
	}
	return bound_tables++;
}

void Binder::PushExpressionBinder(ExpressionBinder *binder) {
	GetActiveBinders().push_back(binder);
}

void Binder::PopExpressionBinder() {
	assert(HasActiveBinder());
	GetActiveBinders().pop_back();
}

void Binder::SetActiveBinder(ExpressionBinder *binder) {
	assert(HasActiveBinder());
	GetActiveBinders().back() = binder;
}

ExpressionBinder *Binder::GetActiveBinder() {
	return GetActiveBinders().back();
}

bool Binder::HasActiveBinder() {
	return GetActiveBinders().size() > 0;
}

vector<ExpressionBinder *> &Binder::GetActiveBinders() {
	if (parent) {
		return parent->GetActiveBinders();
	}
	return active_binders;
}

void Binder::MoveCorrelatedExpressions(Binder &other) {
	MergeCorrelatedColumns(other.correlated_columns);
	other.correlated_columns.clear();
}

void Binder::MergeCorrelatedColumns(vector<CorrelatedColumnInfo> &other) {
	for (idx_t i = 0; i < other.size(); i++) {
		AddCorrelatedColumn(other[i]);
	}
}

void Binder::AddCorrelatedColumn(CorrelatedColumnInfo info) {
	// we only add correlated columns to the list if they are not already there
	if (std::find(correlated_columns.begin(), correlated_columns.end(), info) == correlated_columns.end()) {
		correlated_columns.push_back(info);
	}
}

string Binder::FormatError(ParsedExpression &expr_context, string message) {
	return FormatError(expr_context.query_location, message);
}

string Binder::FormatError(TableRef &ref_context, string message) {
	return FormatError(ref_context.query_location, message);
}

string Binder::FormatError(idx_t query_location, string message) {
	QueryErrorContext context(root_statement, query_location);
	return context.FormatError(message);
}

} // namespace duckdb
