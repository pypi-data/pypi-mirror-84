#include "duckdb/parser/statement/drop_statement.hpp"
#include "duckdb/parser/transformer.hpp"

namespace duckdb {
using namespace std;
using namespace duckdb_libpgquery;

unique_ptr<SQLStatement> Transformer::TransformDrop(PGNode *node) {
	auto stmt = (PGDropStmt *)(node);
	auto result = make_unique<DropStatement>();
	auto &info = *result->info.get();
	assert(stmt);
	if (stmt->objects->length != 1) {
		throw NotImplementedException("Can only drop one object at a time");
	}
	switch (stmt->removeType) {
	case PG_OBJECT_TABLE:
		info.type = CatalogType::TABLE_ENTRY;
		break;
	case PG_OBJECT_SCHEMA:
		info.type = CatalogType::SCHEMA_ENTRY;
		break;
	case PG_OBJECT_INDEX:
		info.type = CatalogType::INDEX_ENTRY;
		break;
	case PG_OBJECT_VIEW:
		info.type = CatalogType::VIEW_ENTRY;
		break;
	case PG_OBJECT_SEQUENCE:
		info.type = CatalogType::SEQUENCE_ENTRY;
		break;
	default:
		throw NotImplementedException("Cannot drop this type yet");
	}

	switch (stmt->removeType) {
	case PG_OBJECT_SCHEMA:
		assert(stmt->objects && stmt->objects->length == 1);
		info.name = ((PGValue *)stmt->objects->head->data.ptr_value)->val.str;
		break;
	default: {
		auto view_list = (PGList *)stmt->objects->head->data.ptr_value;
		if (view_list->length == 2) {
			info.schema = ((PGValue *)view_list->head->data.ptr_value)->val.str;
			info.name = ((PGValue *)view_list->head->next->data.ptr_value)->val.str;
		} else {
			info.name = ((PGValue *)view_list->head->data.ptr_value)->val.str;
		}
		break;
	}
	}
	info.cascade = stmt->behavior == PGDropBehavior::PG_DROP_CASCADE;
	info.if_exists = stmt->missing_ok;
	return move(result);
}

} // namespace duckdb
