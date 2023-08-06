#include "duckdb/parser/statement/select_statement.hpp"
#include "duckdb/parser/transformer.hpp"
#include "duckdb/common/string_util.hpp"

namespace duckdb {
using namespace std;
using namespace duckdb_libpgquery;

unique_ptr<SelectStatement> Transformer::TransformSelect(PGNode *node, bool isSelect) {
	auto stmt = reinterpret_cast<PGSelectStmt *>(node);
	auto result = make_unique<SelectStatement>();

	// Both Insert/Create Table As uses this.
	if (isSelect) {
        if (stmt->intoClause) {
            throw ParserException("SELECT INTO not supported!");
        }
        if (stmt->lockingClause) {
            throw ParserException("SELECT locking clause is not supported!");
        }
	}

    // may contain windows so second
	if (stmt->withClause) {
		TransformCTE(reinterpret_cast<PGWithClause *>(stmt->withClause), *result);
	}

	result->node = TransformSelectNode(stmt);
	return result;
}

} // namespace duckdb
