#include "duckdb/storage/data_table.hpp"

#include "duckdb/catalog/catalog_entry/table_catalog_entry.hpp"
#include "duckdb/common/exception.hpp"
#include "duckdb/common/helper.hpp"
#include "duckdb/common/vector_operations/vector_operations.hpp"
#include "duckdb/execution/expression_executor.hpp"
#include "duckdb/planner/constraints/list.hpp"
#include "duckdb/transaction/transaction.hpp"
#include "duckdb/transaction/transaction_manager.hpp"
#include "duckdb/storage/table/transient_segment.hpp"
#include "duckdb/storage/storage_manager.hpp"
#include "duckdb/main/client_context.hpp"

#include "duckdb/storage/table/morsel_info.hpp"

namespace duckdb {
using namespace std;
using namespace chrono;

DataTable::DataTable(StorageManager &storage, string schema, string table, vector<LogicalType> types_,
                     unique_ptr<vector<unique_ptr<PersistentSegment>>[]> data)
    : info(make_shared<DataTableInfo>(schema, table)), types(types_), storage(storage),
      versions(make_shared<SegmentTree>()), total_rows(0), is_root(true) {
	// set up the segment trees for the column segments
	for (idx_t i = 0; i < types.size(); i++) {
		auto column_data = make_shared<ColumnData>(*storage.buffer_manager, *info);
		column_data->type = types[i];
		column_data->column_idx = i;
		columns.push_back(move(column_data));
	}

	// initialize the table with the existing data from disk, if any
	if (data && data[0].size() > 0) {
		// first append all the segments to the set of column segments
		for (idx_t i = 0; i < types.size(); i++) {
			columns[i]->Initialize(data[i]);
			if (columns[i]->persistent_rows != columns[0]->persistent_rows) {
				throw Exception("Column length mismatch in table load!");
			}
		}
		total_rows = columns[0]->persistent_rows;
		// create empty morsel info's
		// in the future, we should lazily load these from the file as well (once we support deleted flags)
		for (idx_t i = 0; i < total_rows; i += MorselInfo::MORSEL_SIZE) {
			auto segment = make_unique<MorselInfo>(i, MorselInfo::MORSEL_SIZE);
			versions->AppendSegment(move(segment));
		}
	} else {
		// append one (empty) morsel to the table
		auto segment = make_unique<MorselInfo>(0, MorselInfo::MORSEL_SIZE);
		versions->AppendSegment(move(segment));
	}
}

DataTable::DataTable(ClientContext &context, DataTable &parent, ColumnDefinition &new_column, Expression *default_value)
    : info(parent.info), types(parent.types), storage(parent.storage), versions(parent.versions),
      total_rows(parent.total_rows), columns(parent.columns), is_root(true) {
	// prevent any new tuples from being added to the parent
	lock_guard<mutex> parent_lock(parent.append_lock);
	// add the new column to this DataTable
	auto new_column_type = new_column.type;
	idx_t new_column_idx = columns.size();

	types.push_back(new_column_type);
	auto column_data = make_shared<ColumnData>(*storage.buffer_manager, *info);
	column_data->type = new_column_type;
	column_data->column_idx = new_column_idx;
	columns.push_back(move(column_data));

	// fill the column with its DEFAULT value, or NULL if none is specified
	idx_t rows_to_write = total_rows;
	if (rows_to_write > 0) {
		ExpressionExecutor executor;
		DataChunk dummy_chunk;
		Vector result(new_column_type);
		if (!default_value) {
			FlatVector::Nullmask(result).set();
		} else {
			executor.AddExpression(*default_value);
		}

		ColumnAppendState state;
		columns[new_column_idx]->InitializeAppend(state);
		for (idx_t i = 0; i < rows_to_write; i += STANDARD_VECTOR_SIZE) {
			idx_t rows_in_this_vector = MinValue<idx_t>(rows_to_write - i, STANDARD_VECTOR_SIZE);
			if (default_value) {
				dummy_chunk.SetCardinality(rows_in_this_vector);
				executor.ExecuteExpression(dummy_chunk, result);
			}
			columns[new_column_idx]->Append(state, result, rows_in_this_vector);
		}
	}
	// also add this column to client local storage
	Transaction::GetTransaction(context).storage.AddColumn(&parent, this, new_column, default_value);

	// this table replaces the previous table, hence the parent is no longer the root DataTable
	parent.is_root = false;
}

DataTable::DataTable(ClientContext &context, DataTable &parent, idx_t removed_column)
    : info(parent.info), types(parent.types), storage(parent.storage), versions(parent.versions),
      total_rows(parent.total_rows), columns(parent.columns), is_root(true) {
	// prevent any new tuples from being added to the parent
	lock_guard<mutex> parent_lock(parent.append_lock);
	// first check if there are any indexes that exist that point to the removed column
	for (auto &index : info->indexes) {
		for (auto &column_id : index->column_ids) {
			if (column_id == removed_column) {
				throw CatalogException("Cannot drop this column: an index depends on it!");
			} else if (column_id > removed_column) {
				throw CatalogException("Cannot drop this column: an index depends on a column after it!");
			}
		}
	}
	// erase the column from this DataTable
	assert(removed_column < types.size());
	types.erase(types.begin() + removed_column);
	columns.erase(columns.begin() + removed_column);

	// this table replaces the previous table, hence the parent is no longer the root DataTable
	parent.is_root = false;
}

DataTable::DataTable(ClientContext &context, DataTable &parent, idx_t changed_idx, LogicalType target_type,
                     vector<column_t> bound_columns, Expression &cast_expr)
    : info(parent.info), types(parent.types), storage(parent.storage), versions(parent.versions),
      total_rows(parent.total_rows), columns(parent.columns), is_root(true) {

	// prevent any new tuples from being added to the parent
	CreateIndexScanState scan_state;
	parent.InitializeCreateIndexScan(scan_state, bound_columns);

	// first check if there are any indexes that exist that point to the changed column
	for (auto &index : info->indexes) {
		for (auto &column_id : index->column_ids) {
			if (column_id == changed_idx) {
				throw CatalogException("Cannot change the type of this column: an index depends on it!");
			}
		}
	}
	// change the type in this DataTable
	types[changed_idx] = target_type;

	// construct a new column data for this type
	auto column_data = make_shared<ColumnData>(*storage.buffer_manager, *info);
	column_data->type = target_type;
	column_data->column_idx = changed_idx;

	ColumnAppendState append_state;
	column_data->InitializeAppend(append_state);

	// scan the original table, and fill the new column with the transformed value
	auto &transaction = Transaction::GetTransaction(context);

	vector<LogicalType> types;
	for (idx_t i = 0; i < bound_columns.size(); i++) {
		if (bound_columns[i] == COLUMN_IDENTIFIER_ROW_ID) {
			types.push_back(LOGICAL_ROW_TYPE);
		} else {
			types.push_back(parent.types[bound_columns[i]]);
		}
	}

	DataChunk scan_chunk;
	scan_chunk.Initialize(types);

	ExpressionExecutor executor;
	executor.AddExpression(cast_expr);

	Vector append_vector(target_type);
	while (true) {
		// scan the table
		scan_chunk.Reset();
		parent.CreateIndexScan(scan_state, bound_columns, scan_chunk);
		if (scan_chunk.size() == 0) {
			break;
		}
		// execute the expression
		executor.ExecuteExpression(scan_chunk, append_vector);
		column_data->Append(append_state, append_vector, scan_chunk.size());
	}
	// also add this column to client local storage
	transaction.storage.ChangeType(&parent, this, changed_idx, target_type, bound_columns, cast_expr);

	columns[changed_idx] = move(column_data);

	// this table replaces the previous table, hence the parent is no longer the root DataTable
	parent.is_root = false;
}

//===--------------------------------------------------------------------===//
// Scan
//===--------------------------------------------------------------------===//
void DataTable::InitializeScan(TableScanState &state, const vector<column_t> &column_ids,
                               unordered_map<idx_t, vector<TableFilter>> *table_filters) {
	// initialize a column scan state for each column
	state.column_scans = unique_ptr<ColumnScanState[]>(new ColumnScanState[column_ids.size()]);
	for (idx_t i = 0; i < column_ids.size(); i++) {
		auto column = column_ids[i];
		if (column != COLUMN_IDENTIFIER_ROW_ID) {
			columns[column]->InitializeScan(state.column_scans[i]);
		} else {
			state.column_scans[i].current = nullptr;
		}
	}
	// initialize the chunk scan state
	state.column_count = column_ids.size();
	state.current_row = 0;
	state.base_row = 0;
	state.max_row = total_rows;
	state.version_info = (MorselInfo *)versions->GetRootSegment();
	if (table_filters && table_filters->size() > 0) {
		state.adaptive_filter = make_unique<AdaptiveFilter>(*table_filters);
	}
}

void DataTable::InitializeScan(Transaction &transaction, TableScanState &state, const vector<column_t> &column_ids,
                               unordered_map<idx_t, vector<TableFilter>> *table_filters) {
	InitializeScan(state, column_ids, table_filters);
	transaction.storage.InitializeScan(this, state.local_state);
}

void DataTable::InitializeScanWithOffset(TableScanState &state, const vector<column_t> &column_ids,
                                         unordered_map<idx_t, vector<TableFilter>> *table_filters, idx_t start_row,
                                         idx_t end_row) {
	assert(start_row % STANDARD_VECTOR_SIZE == 0);
	assert(end_row > start_row);
	idx_t vector_offset = start_row / STANDARD_VECTOR_SIZE;
	// initialize a column scan state for each column
	state.column_scans = unique_ptr<ColumnScanState[]>(new ColumnScanState[column_ids.size()]);
	for (idx_t i = 0; i < column_ids.size(); i++) {
		auto column = column_ids[i];
		if (column != COLUMN_IDENTIFIER_ROW_ID) {
			columns[column]->InitializeScanWithOffset(state.column_scans[i], vector_offset);
		} else {
			state.column_scans[i].current = nullptr;
		}
	}

	// initialize the chunk scan state
	state.column_count = column_ids.size();
	state.current_row = start_row;
	state.base_row = start_row;
	state.max_row = end_row;
	state.version_info = (MorselInfo *)versions->GetSegment(state.current_row);
	if (table_filters && table_filters->size() > 0 && !state.adaptive_filter) {
		state.adaptive_filter = make_unique<AdaptiveFilter>(*table_filters);
	}
}

idx_t DataTable::MaxThreads(ClientContext &context) {
	idx_t PARALLEL_SCAN_VECTOR_COUNT = 100;
	if (context.force_parallelism) {
		PARALLEL_SCAN_VECTOR_COUNT = 1;
	}
	idx_t PARALLEL_SCAN_TUPLE_COUNT = STANDARD_VECTOR_SIZE * PARALLEL_SCAN_VECTOR_COUNT;

	return total_rows / PARALLEL_SCAN_TUPLE_COUNT + 1;
}

void DataTable::InitializeParallelScan(ParallelTableScanState &state) {
	state.current_row = 0;
	state.transaction_local_data = false;
}

bool DataTable::NextParallelScan(ClientContext &context, ParallelTableScanState &state, TableScanState &scan_state,
                                 const vector<column_t> &column_ids,
                                 unordered_map<idx_t, vector<TableFilter>> *table_filters) {
	idx_t PARALLEL_SCAN_VECTOR_COUNT = 100;
	if (context.force_parallelism) {
		PARALLEL_SCAN_VECTOR_COUNT = 1;
	}
	idx_t PARALLEL_SCAN_TUPLE_COUNT = STANDARD_VECTOR_SIZE * PARALLEL_SCAN_VECTOR_COUNT;

	if (state.current_row < total_rows) {
		idx_t next = MinValue(state.current_row + PARALLEL_SCAN_TUPLE_COUNT, total_rows);

		// scan a morsel from the persistent rows
		InitializeScanWithOffset(scan_state, column_ids, table_filters, state.current_row, next);

		state.current_row = next;
		return true;
	} else if (!state.transaction_local_data) {
		auto &transaction = Transaction::GetTransaction(context);
		// create a task for scanning the local data
		scan_state.current_row = 0;
		scan_state.base_row = 0;
		scan_state.max_row = 0;
		transaction.storage.InitializeScan(this, scan_state.local_state);
		state.transaction_local_data = true;
		return true;
	} else {
		// finished all scans: no more scans remaining
		return false;
	}
}

void DataTable::Scan(Transaction &transaction, DataChunk &result, TableScanState &state, vector<column_t> &column_ids,
                     unordered_map<idx_t, vector<TableFilter>> &table_filters) {
	// scan the persistent segments
	while (ScanBaseTable(transaction, result, state, column_ids, state.current_row, state.max_row, table_filters)) {
		if (result.size() > 0) {
			return;
		}
		result.Reset();
	}

	// scan the transaction-local segments
	transaction.storage.Scan(state.local_state, column_ids, result, &table_filters);
}

template <class T> bool checkZonemap(TableScanState &state, TableFilter &table_filter, T constant) {
	T *min = (T *)state.column_scans[table_filter.column_index].current->stats.minimum.get();
	T *max = (T *)state.column_scans[table_filter.column_index].current->stats.maximum.get();
	switch (table_filter.comparison_type) {
	case ExpressionType::COMPARE_EQUAL:
		return constant >= *min && constant <= *max;
	case ExpressionType::COMPARE_GREATERTHANOREQUALTO:
		return constant <= *max;
	case ExpressionType::COMPARE_GREATERTHAN:
		return constant < *max;
	case ExpressionType::COMPARE_LESSTHANOREQUALTO:
		return constant >= *min;
	case ExpressionType::COMPARE_LESSTHAN:
		return constant > *min;
	default:
		throw NotImplementedException("Operation not implemented");
	}
}

bool checkZonemapString(TableScanState &state, TableFilter &table_filter, const char *constant) {
	char *min = (char *)state.column_scans[table_filter.column_index].current->stats.minimum.get();
	char *max = (char *)state.column_scans[table_filter.column_index].current->stats.maximum.get();
	int min_comp = strcmp(min, constant);
	int max_comp = strcmp(max, constant);
	switch (table_filter.comparison_type) {
	case ExpressionType::COMPARE_EQUAL:
		return min_comp <= 0 && max_comp >= 0;
	case ExpressionType::COMPARE_GREATERTHANOREQUALTO:
	case ExpressionType::COMPARE_GREATERTHAN:
		return max_comp >= 0;
	case ExpressionType::COMPARE_LESSTHAN:
	case ExpressionType::COMPARE_LESSTHANOREQUALTO:
		return min_comp <= 0;
	default:
		throw NotImplementedException("Operation not implemented");
	}
}

bool DataTable::CheckZonemap(TableScanState &state, unordered_map<idx_t, vector<TableFilter>> &table_filters,
                             idx_t &current_row) {
	for (auto &table_filter : table_filters) {
		for (auto &predicate_constant : table_filter.second) {
			bool readSegment = true;

			if (!state.column_scans[predicate_constant.column_index].segment_checked) {
				state.column_scans[predicate_constant.column_index].segment_checked = true;
				if (!state.column_scans[predicate_constant.column_index].current) {
					return true;
				}
				switch (state.column_scans[predicate_constant.column_index].current->type) {
				case PhysicalType::INT8: {
					int8_t constant = predicate_constant.constant.value_.tinyint;
					readSegment = checkZonemap<int8_t>(state, predicate_constant, constant);
					break;
				}
				case PhysicalType::INT16: {
					int16_t constant = predicate_constant.constant.value_.smallint;
					readSegment = checkZonemap<int16_t>(state, predicate_constant, constant);
					break;
				}
				case PhysicalType::INT32: {
					int32_t constant = predicate_constant.constant.value_.integer;
					readSegment = checkZonemap<int32_t>(state, predicate_constant, constant);
					break;
				}
				case PhysicalType::INT64: {
					int64_t constant = predicate_constant.constant.value_.bigint;
					readSegment = checkZonemap<int64_t>(state, predicate_constant, constant);
					break;
				}
				case PhysicalType::INT128: {
					auto constant = predicate_constant.constant.value_.hugeint;
					readSegment = checkZonemap<hugeint_t>(state, predicate_constant, constant);
					break;
				}
				case PhysicalType::FLOAT: {
					float constant = predicate_constant.constant.value_.float_;
					readSegment = checkZonemap<float>(state, predicate_constant, constant);
					break;
				}
				case PhysicalType::DOUBLE: {
					double constant = predicate_constant.constant.value_.double_;
					readSegment = checkZonemap<double>(state, predicate_constant, constant);
					break;
				}
				case PhysicalType::VARCHAR: {
					//! we can only compare the first 7 bytes
					size_t value_size = predicate_constant.constant.str_value.size() > 7
					                        ? 7
					                        : predicate_constant.constant.str_value.size();
					string constant;
					for (size_t i = 0; i < value_size; i++) {
						constant += predicate_constant.constant.str_value[i];
					}
					readSegment = checkZonemapString(state, predicate_constant, constant.c_str());
					break;
				}
				default:
					throw NotImplementedException("Unimplemented type for zonemaps");
				}
			}
			if (!readSegment) {
				//! We can skip this partition
				idx_t vectorsToSkip =
				    ceil((double)(state.column_scans[predicate_constant.column_index].current->count +
				                  state.column_scans[predicate_constant.column_index].current->start - current_row) /
				         STANDARD_VECTOR_SIZE);
				for (idx_t i = 0; i < vectorsToSkip; ++i) {
					state.NextVector();
					current_row += STANDARD_VECTOR_SIZE;
				}
				return false;
			}
		}
	}

	return true;
}

bool DataTable::ScanBaseTable(Transaction &transaction, DataChunk &result, TableScanState &state,
                              const vector<column_t> &column_ids, idx_t &current_row, idx_t max_row,
                              unordered_map<idx_t, vector<TableFilter>> &table_filters) {
	if (current_row >= max_row) {
		// exceeded the amount of rows to scan
		return false;
	}
	idx_t max_count = MinValue<idx_t>(STANDARD_VECTOR_SIZE, max_row - current_row);
	idx_t vector_offset = (current_row - state.base_row) / STANDARD_VECTOR_SIZE;
	//! first check the zonemap if we have to scan this partition
	if (!CheckZonemap(state, table_filters, current_row)) {
		return true;
	}
	// second, scan the version chunk manager to figure out which tuples to load for this transaction
	SelectionVector valid_sel(STANDARD_VECTOR_SIZE);
	if (vector_offset >= MorselInfo::MORSEL_VECTOR_COUNT) {
		state.version_info = (MorselInfo *)state.version_info->next.get();
		state.base_row += MorselInfo::MORSEL_SIZE;
		vector_offset = 0;
	}
	idx_t count = state.version_info->GetSelVector(transaction, vector_offset, valid_sel, max_count);
	if (count == 0) {
		// nothing to scan for this vector, skip the entire vector
		state.NextVector();
		current_row += STANDARD_VECTOR_SIZE;
		return true;
	}
	idx_t approved_tuple_count = count;
	if (count == max_count && table_filters.empty()) {
		//! If we don't have any deleted tuples or filters we can just run a regular scan
		for (idx_t i = 0; i < column_ids.size(); i++) {
			auto column = column_ids[i];
			if (column == COLUMN_IDENTIFIER_ROW_ID) {
				// scan row id
				assert(result.data[i].type.InternalType() == ROW_TYPE);
				result.data[i].Sequence(current_row, 1);
			} else {
				columns[column]->Scan(transaction, state.column_scans[i], result.data[i]);
			}
		}
	} else {
		SelectionVector sel;

		if (count != max_count) {
			sel.Initialize(valid_sel);
		} else {
			sel.Initialize(FlatVector::IncrementalSelectionVector);
		}
		//! First, we scan the columns with filters, fetch their data and generate a selection vector.
		//! get runtime statistics
		auto start_time = high_resolution_clock::now();
		for (idx_t i = 0; i < table_filters.size(); i++) {
			auto tf_idx = state.adaptive_filter->permutation[i];
			auto col_idx = column_ids[tf_idx];
			columns[col_idx]->Select(transaction, state.column_scans[tf_idx], result.data[tf_idx], sel,
			                         approved_tuple_count, table_filters[tf_idx]);
		}
		for (auto &table_filter : table_filters) {
			result.data[table_filter.first].Slice(sel, approved_tuple_count);
		}
		//! Now we use the selection vector to fetch data for the other columns.
		for (idx_t i = 0; i < column_ids.size(); i++) {
			if (table_filters.find(i) == table_filters.end()) {
				auto column = column_ids[i];
				if (column == COLUMN_IDENTIFIER_ROW_ID) {
					assert(result.data[i].type.InternalType() == PhysicalType::INT64);
					result.data[i].vector_type = VectorType::FLAT_VECTOR;
					auto result_data = (int64_t *)FlatVector::GetData(result.data[i]);
					for (size_t sel_idx = 0; sel_idx < approved_tuple_count; sel_idx++) {
						result_data[sel_idx] = current_row + sel.get_index(sel_idx);
					}
				} else {
					columns[column]->FilterScan(transaction, state.column_scans[i], result.data[i], sel,
					                            approved_tuple_count);
				}
			}
		}
		auto end_time = high_resolution_clock::now();
		if (state.adaptive_filter && table_filters.size() > 1) {
			state.adaptive_filter->AdaptRuntimeStatistics(
			    duration_cast<duration<double>>(end_time - start_time).count());
		}
	}

	result.SetCardinality(approved_tuple_count);
	current_row += STANDARD_VECTOR_SIZE;
	return true;
}

//===--------------------------------------------------------------------===//
// Fetch
//===--------------------------------------------------------------------===//
void DataTable::Fetch(Transaction &transaction, DataChunk &result, vector<column_t> &column_ids,
                      Vector &row_identifiers, idx_t fetch_count, ColumnFetchState &state) {
	// first figure out which row identifiers we should use for this transaction by looking at the VersionManagers
	row_t rows[STANDARD_VECTOR_SIZE];
	idx_t count = FetchRows(transaction, row_identifiers, fetch_count, rows);
	if (count == 0) {
		// no rows to use
		return;
	}
	// for each of the remaining rows, now fetch the data
	result.SetCardinality(count);
	for (idx_t col_idx = 0; col_idx < column_ids.size(); col_idx++) {
		auto column = column_ids[col_idx];
		if (column == COLUMN_IDENTIFIER_ROW_ID) {
			// row id column: fill in the row ids
			assert(result.data[col_idx].type.InternalType() == PhysicalType::INT64);
			result.data[col_idx].vector_type = VectorType::FLAT_VECTOR;
			auto data = FlatVector::GetData<row_t>(result.data[col_idx]);
			for (idx_t i = 0; i < count; i++) {
				data[i] = rows[i];
			}
		} else {
			// regular column: fetch data from the base column
			for (idx_t i = 0; i < count; i++) {
				auto row_id = rows[i];
				columns[column]->FetchRow(state, transaction, row_id, result.data[col_idx], i);
			}
		}
	}
}

idx_t DataTable::FetchRows(Transaction &transaction, Vector &row_identifiers, idx_t fetch_count, row_t result_rows[]) {
	assert(row_identifiers.type.InternalType() == ROW_TYPE);

	// now iterate over the row ids and figure out which rows to use
	idx_t count = 0;

	auto row_ids = FlatVector::GetData<row_t>(row_identifiers);
	for (idx_t i = 0; i < fetch_count; i++) {
		auto row_id = row_ids[i];
		auto segment = (MorselInfo *)versions->GetSegment(row_id);
		bool use_row = segment->Fetch(transaction, row_id - segment->start);
		if (use_row) {
			// row is not deleted; use the row
			result_rows[count++] = row_id;
		}
	}
	return count;
}

//===--------------------------------------------------------------------===//
// Append
//===--------------------------------------------------------------------===//
static void VerifyNotNullConstraint(TableCatalogEntry &table, Vector &vector, idx_t count, string &col_name) {
	if (VectorOperations::HasNull(vector, count)) {
		throw ConstraintException("NOT NULL constraint failed: %s.%s", table.name, col_name);
	}
}

static void VerifyCheckConstraint(TableCatalogEntry &table, Expression &expr, DataChunk &chunk) {
	ExpressionExecutor executor(expr);
	Vector result(LogicalType::INTEGER);
	try {
		executor.ExecuteExpression(chunk, result);
	} catch (Exception &ex) {
		throw ConstraintException("CHECK constraint failed: %s (Error: %s)", table.name, ex.what());
	} catch (...) {
		throw ConstraintException("CHECK constraint failed: %s (Unknown Error)", table.name);
	}
	VectorData vdata;
	result.Orrify(chunk.size(), vdata);

	auto dataptr = (int32_t *)vdata.data;
	for (idx_t i = 0; i < chunk.size(); i++) {
		auto idx = vdata.sel->get_index(i);
		if (!(*vdata.nullmask)[idx] && dataptr[idx] == 0) {
			throw ConstraintException("CHECK constraint failed: %s", table.name);
		}
	}
}

void DataTable::VerifyAppendConstraints(TableCatalogEntry &table, DataChunk &chunk) {
	for (auto &constraint : table.bound_constraints) {
		switch (constraint->type) {
		case ConstraintType::NOT_NULL: {
			auto &not_null = *reinterpret_cast<BoundNotNullConstraint *>(constraint.get());
			VerifyNotNullConstraint(table, chunk.data[not_null.index], chunk.size(),
			                        table.columns[not_null.index].name);
			break;
		}
		case ConstraintType::CHECK: {
			auto &check = *reinterpret_cast<BoundCheckConstraint *>(constraint.get());
			VerifyCheckConstraint(table, *check.expression, chunk);
			break;
		}
		case ConstraintType::UNIQUE: {
			//! check whether or not the chunk can be inserted into the indexes
			for (auto &index : info->indexes) {
				index->VerifyAppend(chunk);
			}
			break;
		}
		case ConstraintType::FOREIGN_KEY:
		default:
			throw NotImplementedException("Constraint type not implemented!");
		}
	}
}

void DataTable::Append(TableCatalogEntry &table, ClientContext &context, DataChunk &chunk) {
	if (chunk.size() == 0) {
		return;
	}
	if (chunk.column_count() != table.columns.size()) {
		throw CatalogException("Mismatch in column count for append");
	}
	if (!is_root) {
		throw TransactionException("Transaction conflict: adding entries to a table that has been altered!");
	}

	chunk.Verify();

	// verify any constraints on the new chunk
	VerifyAppendConstraints(table, chunk);

	// append to the transaction local data
	auto &transaction = Transaction::GetTransaction(context);
	transaction.storage.Append(this, chunk);
}

void DataTable::InitializeAppend(Transaction &transaction, TableAppendState &state, idx_t append_count) {
	// obtain the append lock for this table
	state.append_lock = unique_lock<mutex>(append_lock);
	if (!is_root) {
		throw TransactionException("Transaction conflict: adding entries to a table that has been altered!");
	}
	// obtain locks on all indexes for the table
	state.index_locks = unique_ptr<IndexLock[]>(new IndexLock[info->indexes.size()]);
	for (idx_t i = 0; i < info->indexes.size(); i++) {
		info->indexes[i]->InitializeLock(state.index_locks[i]);
	}
	// for each column, initialize the append state
	state.states = unique_ptr<ColumnAppendState[]>(new ColumnAppendState[types.size()]);
	for (idx_t i = 0; i < types.size(); i++) {
		columns[i]->InitializeAppend(state.states[i]);
	}
	state.row_start = total_rows;
	state.current_row = state.row_start;

	// start writing to the morsels
	lock_guard<mutex> morsel_lock(versions->node_lock);
	auto last_morsel = (MorselInfo *)versions->GetLastSegment();
	assert(last_morsel->start <= (idx_t)state.row_start);
	idx_t current_position = state.row_start - last_morsel->start;
	idx_t remaining = append_count;
	while (true) {
		idx_t remaining_in_morsel = MorselInfo::MORSEL_SIZE - current_position;
		idx_t to_write = MinValue<idx_t>(remaining, remaining_in_morsel);
		remaining -= to_write;
		if (to_write > 0) {
			// write to the last morsel
			auto morsel = (MorselInfo *)versions->GetLastSegment();
			morsel->Append(transaction, current_position, to_write, transaction.transaction_id);
		}

		current_position = 0;
		if (remaining > 0) {
			idx_t start = last_morsel->start + MorselInfo::MORSEL_SIZE;
			auto morsel = make_unique<MorselInfo>(start, MorselInfo::MORSEL_SIZE);
			last_morsel = morsel.get();
			versions->AppendSegment(move(morsel));
		} else {
			break;
		}
	}
	total_rows += append_count;
}

void DataTable::Append(Transaction &transaction, DataChunk &chunk, TableAppendState &state) {
	assert(is_root);
	assert(chunk.column_count() == types.size());
	chunk.Verify();

	// append the physical data to each of the entries
	for (idx_t i = 0; i < types.size(); i++) {
		columns[i]->Append(state.states[i], chunk.data[i], chunk.size());
	}
	state.current_row += chunk.size();
}

void DataTable::ScanTableSegment(idx_t row_start, idx_t count, std::function<void(DataChunk &chunk)> function) {
	idx_t end = row_start + count;

	vector<column_t> column_ids;
	vector<LogicalType> types;
	for (idx_t i = 0; i < columns.size(); i++) {
		column_ids.push_back(i);
		types.push_back(columns[i]->type);
	}
	DataChunk chunk;
	chunk.Initialize(types);

	CreateIndexScanState state;

	idx_t row_start_aligned = row_start / STANDARD_VECTOR_SIZE * STANDARD_VECTOR_SIZE;
	InitializeScanWithOffset(state, column_ids, nullptr, row_start_aligned, row_start + count);

	while (true) {
		idx_t current_row = state.current_row;
		CreateIndexScan(state, column_ids, chunk);
		if (chunk.size() == 0) {
			break;
		}
		idx_t end_row = state.current_row;
		// figure out if we need to write the entire chunk or just part of it
		idx_t chunk_start = current_row < row_start ? row_start : current_row;
		idx_t chunk_end = end_row > end ? end : end_row;
		idx_t chunk_count = chunk_end - chunk_start;
		if (chunk_count != chunk.size()) {
			// need to slice the chunk before insert
			SelectionVector sel(chunk_start % STANDARD_VECTOR_SIZE, chunk_count);
			chunk.Slice(sel, chunk_count);
		}
		function(chunk);
		chunk.Reset();
	}
}

void DataTable::WriteToLog(WriteAheadLog &log, idx_t row_start, idx_t count) {
	log.WriteSetTable(info->schema, info->table);
	ScanTableSegment(row_start, count, [&](DataChunk &chunk) { log.WriteInsert(chunk); });
}

void DataTable::CommitAppend(transaction_t commit_id, idx_t row_start, idx_t count) {
	lock_guard<mutex> lock(append_lock);

	auto morsel = (MorselInfo *)versions->GetSegment(row_start);
	idx_t current_row = row_start;
	idx_t remaining = count;
	while (true) {
		idx_t start_in_morsel = current_row - morsel->start;
		idx_t append_count = MinValue<idx_t>(morsel->count - start_in_morsel, remaining);

		morsel->CommitAppend(commit_id, start_in_morsel, append_count);

		current_row += append_count;
		remaining -= append_count;
		if (remaining == 0) {
			break;
		}
		morsel = (MorselInfo *)morsel->next.get();
	}
	info->cardinality += count;
}

void DataTable::RevertAppendInternal(idx_t start_row, idx_t count) {
	if (count == 0) {
		// nothing to revert!
		return;
	}

	if (total_rows != start_row + count) {
		// interleaved append: don't do anything
		// in this case the rows will stay as "inserted by transaction X", but will never be committed
		// they will never be used by any other transaction and will essentially leave a gap
		// this situation is rare, and as such we don't care about optimizing it (yet?)
		// it only happens if C1 appends a lot of data -> C2 appends a lot of data -> C1 rolls back
		return;
	}
	// adjust the cardinality
	info->cardinality = start_row;
	total_rows = start_row;
	assert(is_root);
	// revert changes in the base columns
	for (idx_t i = 0; i < types.size(); i++) {
		columns[i]->RevertAppend(start_row);
	}
	// revert appends made to morsels
	lock_guard<mutex> tree_lock(versions->node_lock);
	// find the segment index that the current row belongs to
	idx_t segment_index = versions->GetSegmentIndex(start_row);
	auto segment = versions->nodes[segment_index].node;
	auto &info = (MorselInfo &)*segment;

	// remove any segments AFTER this segment: they should be deleted entirely
	if (segment_index < versions->nodes.size() - 1) {
		versions->nodes.erase(versions->nodes.begin() + segment_index + 1, versions->nodes.end());
	}
	info.next = nullptr;
	info.RevertAppend(start_row);
}

void DataTable::RevertAppend(idx_t start_row, idx_t count) {
	lock_guard<mutex> lock(append_lock);
	if (info->indexes.size() > 0) {
		auto index_locks = unique_ptr<IndexLock[]>(new IndexLock[info->indexes.size()]);
		for (idx_t i = 0; i < info->indexes.size(); i++) {
			info->indexes[i]->InitializeLock(index_locks[i]);
		}
		idx_t current_row_base = start_row;
		row_t row_data[STANDARD_VECTOR_SIZE];
		Vector row_identifiers(LOGICAL_ROW_TYPE, (data_ptr_t)row_data);
		ScanTableSegment(start_row, count, [&](DataChunk &chunk) {
			for (idx_t i = 0; i < chunk.size(); i++) {
				row_data[i] = current_row_base + i;
			}
			for (idx_t i = 0; i < info->indexes.size(); i++) {
				info->indexes[i]->Delete(index_locks[i], chunk, row_identifiers);
			}
			current_row_base += chunk.size();
		});
	}
	RevertAppendInternal(start_row, count);
}

//===--------------------------------------------------------------------===//
// Indexes
//===--------------------------------------------------------------------===//
bool DataTable::AppendToIndexes(TableAppendState &state, DataChunk &chunk, row_t row_start) {
	assert(is_root);
	if (info->indexes.size() == 0) {
		return true;
	}
	// first generate the vector of row identifiers
	Vector row_identifiers(LOGICAL_ROW_TYPE);
	VectorOperations::GenerateSequence(row_identifiers, chunk.size(), row_start, 1);

	idx_t failed_index = INVALID_INDEX;
	// now append the entries to the indices
	for (idx_t i = 0; i < info->indexes.size(); i++) {
		if (!info->indexes[i]->Append(state.index_locks[i], chunk, row_identifiers)) {
			failed_index = i;
			break;
		}
	}
	if (failed_index != INVALID_INDEX) {
		// constraint violation!
		// remove any appended entries from previous indexes (if any)
		for (idx_t i = 0; i < failed_index; i++) {
			info->indexes[i]->Delete(state.index_locks[i], chunk, row_identifiers);
		}
		return false;
	}
	return true;
}

void DataTable::RemoveFromIndexes(TableAppendState &state, DataChunk &chunk, row_t row_start) {
	assert(is_root);
	if (info->indexes.size() == 0) {
		return;
	}
	// first generate the vector of row identifiers
	Vector row_identifiers(LOGICAL_ROW_TYPE);
	VectorOperations::GenerateSequence(row_identifiers, chunk.size(), row_start, 1);

	// now remove the entries from the indices
	RemoveFromIndexes(state, chunk, row_identifiers);
}

void DataTable::RemoveFromIndexes(TableAppendState &state, DataChunk &chunk, Vector &row_identifiers) {
	assert(is_root);
	for (idx_t i = 0; i < info->indexes.size(); i++) {
		info->indexes[i]->Delete(state.index_locks[i], chunk, row_identifiers);
	}
}

void DataTable::RemoveFromIndexes(Vector &row_identifiers, idx_t count) {
	assert(is_root);
	auto row_ids = FlatVector::GetData<row_t>(row_identifiers);
	// create a selection vector from the row_ids
	SelectionVector sel(STANDARD_VECTOR_SIZE);
	for (idx_t i = 0; i < count; i++) {
		sel.set_index(i, row_ids[i] % STANDARD_VECTOR_SIZE);
	}

	// fetch the data for these row identifiers
	DataChunk result;
	result.Initialize(types);
	// FIXME: we do not need to fetch all columns, only the columns required by the indices!
	auto states = unique_ptr<ColumnScanState[]>(new ColumnScanState[types.size()]);
	for (idx_t i = 0; i < types.size(); i++) {
		columns[i]->Fetch(states[i], row_ids[0], result.data[i]);
	}
	result.Slice(sel, count);
	for (auto &index : info->indexes) {
		index->Delete(result, row_identifiers);
	}
}

//===--------------------------------------------------------------------===//
// Delete
//===--------------------------------------------------------------------===//
void DataTable::Delete(TableCatalogEntry &table, ClientContext &context, Vector &row_identifiers, idx_t count) {
	assert(row_identifiers.type.InternalType() == ROW_TYPE);
	if (count == 0) {
		return;
	}

	auto &transaction = Transaction::GetTransaction(context);

	row_identifiers.Normalify(count);
	auto ids = FlatVector::GetData<row_t>(row_identifiers);
	auto first_id = ids[0];

	if (first_id >= MAX_ROW_ID) {
		// deletion is in transaction-local storage: push delete into local chunk collection
		transaction.storage.Delete(this, row_identifiers, count);
	} else {
		auto morsel = (MorselInfo *)versions->GetSegment(first_id);
		morsel->Delete(transaction, this, row_identifiers, count);
	}
}

//===--------------------------------------------------------------------===//
// Update
//===--------------------------------------------------------------------===//
static void CreateMockChunk(vector<LogicalType> &types, vector<column_t> &column_ids, DataChunk &chunk,
                            DataChunk &mock_chunk) {
	// construct a mock DataChunk
	mock_chunk.InitializeEmpty(types);
	for (column_t i = 0; i < column_ids.size(); i++) {
		mock_chunk.data[column_ids[i]].Reference(chunk.data[i]);
	}
	mock_chunk.SetCardinality(chunk.size());
}

static bool CreateMockChunk(TableCatalogEntry &table, vector<column_t> &column_ids,
                            unordered_set<column_t> &desired_column_ids, DataChunk &chunk, DataChunk &mock_chunk) {
	idx_t found_columns = 0;
	// check whether the desired columns are present in the UPDATE clause
	for (column_t i = 0; i < column_ids.size(); i++) {
		if (desired_column_ids.find(column_ids[i]) != desired_column_ids.end()) {
			found_columns++;
		}
	}
	if (found_columns == 0) {
		// no columns were found: no need to check the constraint again
		return false;
	}
	if (found_columns != desired_column_ids.size()) {
		// FIXME: not all columns in UPDATE clause are present!
		// this should not be triggered at all as the binder should add these columns
		throw InternalException("Not all columns required for the CHECK constraint are present in the UPDATED chunk!");
	}
	// construct a mock DataChunk
	auto types = table.GetTypes();
	CreateMockChunk(types, column_ids, chunk, mock_chunk);
	return true;
}

void DataTable::VerifyUpdateConstraints(TableCatalogEntry &table, DataChunk &chunk, vector<column_t> &column_ids) {
	for (auto &constraint : table.bound_constraints) {
		switch (constraint->type) {
		case ConstraintType::NOT_NULL: {
			auto &not_null = *reinterpret_cast<BoundNotNullConstraint *>(constraint.get());
			// check if the constraint is in the list of column_ids
			for (idx_t i = 0; i < column_ids.size(); i++) {
				if (column_ids[i] == not_null.index) {
					// found the column id: check the data in
					VerifyNotNullConstraint(table, chunk.data[i], chunk.size(), table.columns[not_null.index].name);
					break;
				}
			}
			break;
		}
		case ConstraintType::CHECK: {
			auto &check = *reinterpret_cast<BoundCheckConstraint *>(constraint.get());

			DataChunk mock_chunk;
			if (CreateMockChunk(table, column_ids, check.bound_columns, chunk, mock_chunk)) {
				VerifyCheckConstraint(table, *check.expression, mock_chunk);
			}
			break;
		}
		case ConstraintType::UNIQUE:
		case ConstraintType::FOREIGN_KEY:
			break;
		default:
			throw NotImplementedException("Constraint type not implemented!");
		}
	}
	// update should not be called for indexed columns!
	// instead update should have been rewritten to delete + update on higher layer
#ifdef DEBUG
	for (idx_t i = 0; i < info->indexes.size(); i++) {
		assert(!info->indexes[i]->IndexIsUpdated(column_ids));
	}
#endif
}

void DataTable::Update(TableCatalogEntry &table, ClientContext &context, Vector &row_ids, vector<column_t> &column_ids,
                       DataChunk &updates) {
	assert(row_ids.type.InternalType() == ROW_TYPE);

	updates.Verify();
	if (updates.size() == 0) {
		return;
	}

	// first verify that no constraints are violated
	VerifyUpdateConstraints(table, updates, column_ids);

	// now perform the actual update
	auto &transaction = Transaction::GetTransaction(context);

	updates.Normalify();
	row_ids.Normalify(updates.size());
	auto first_id = FlatVector::GetValue<row_t>(row_ids, 0);
	if (first_id >= MAX_ROW_ID) {
		// update is in transaction-local storage: push update into local storage
		transaction.storage.Update(this, row_ids, column_ids, updates);
		return;
	}

	for (idx_t i = 0; i < column_ids.size(); i++) {
		auto column = column_ids[i];
		assert(column != COLUMN_IDENTIFIER_ROW_ID);

		columns[column]->Update(transaction, updates.data[i], row_ids, updates.size());
	}
}

//===--------------------------------------------------------------------===//
// Create Index Scan
//===--------------------------------------------------------------------===//
void DataTable::InitializeCreateIndexScan(CreateIndexScanState &state, const vector<column_t> &column_ids) {
	// we grab the append lock to make sure nothing is appended until AFTER we finish the index scan
	state.append_lock = unique_lock<mutex>(append_lock);
	state.delete_lock = unique_lock<mutex>(versions->node_lock);

	InitializeScan(state, column_ids);
}

void DataTable::CreateIndexScan(CreateIndexScanState &state, const vector<column_t> &column_ids, DataChunk &result) {
	// scan the persistent segments
	if (ScanCreateIndex(state, column_ids, result, state.current_row, state.max_row)) {
		return;
	}
}

bool DataTable::ScanCreateIndex(CreateIndexScanState &state, const vector<column_t> &column_ids, DataChunk &result,
                                idx_t &current_row, idx_t max_row) {
	if (current_row >= max_row) {
		return false;
	}
	idx_t count = MinValue<idx_t>(STANDARD_VECTOR_SIZE, max_row - current_row);

	// scan the base columns to fetch the actual data
	// note that we insert all data into the index, even if it is marked as deleted
	// FIXME: tuples that are already "cleaned up" do not need to be inserted into the index!
	for (idx_t i = 0; i < column_ids.size(); i++) {
		auto column = column_ids[i];
		if (column == COLUMN_IDENTIFIER_ROW_ID) {
			// scan row id
			assert(result.data[i].type.InternalType() == ROW_TYPE);
			result.data[i].Sequence(current_row, 1);
		} else {
			// scan actual base column
			columns[column]->IndexScan(state.column_scans[i], result.data[i]);
		}
	}
	result.SetCardinality(count);

	current_row += STANDARD_VECTOR_SIZE;
	return count > 0;
}

void DataTable::AddIndex(unique_ptr<Index> index, vector<unique_ptr<Expression>> &expressions) {
	DataChunk result;
	result.Initialize(index->logical_types);

	DataChunk intermediate;
	vector<LogicalType> intermediate_types;
	auto column_ids = index->column_ids;
	column_ids.push_back(COLUMN_IDENTIFIER_ROW_ID);
	for (auto &id : index->column_ids) {
		intermediate_types.push_back(types[id]);
	}
	intermediate_types.push_back(LOGICAL_ROW_TYPE);
	intermediate.Initialize(intermediate_types);

	// initialize an index scan
	CreateIndexScanState state;
	InitializeCreateIndexScan(state, column_ids);

	if (!is_root) {
		throw TransactionException("Transaction conflict: cannot add an index to a table that has been altered!");
	}

	// now start incrementally building the index
	IndexLock lock;
	index->InitializeLock(lock);
	ExpressionExecutor executor(expressions);
	while (true) {
		intermediate.Reset();
		// scan a new chunk from the table to index
		CreateIndexScan(state, column_ids, intermediate);
		if (intermediate.size() == 0) {
			// finished scanning for index creation
			// release all locks
			break;
		}
		// resolve the expressions for this chunk
		executor.Execute(intermediate, result);

		// insert into the index
		if (!index->Insert(lock, result, intermediate.data[intermediate.column_count() - 1])) {
			throw ConstraintException("Cant create unique index, table contains duplicate data on indexed column(s)");
		}
	}
	info->indexes.push_back(move(index));
}

} // namespace duckdb
