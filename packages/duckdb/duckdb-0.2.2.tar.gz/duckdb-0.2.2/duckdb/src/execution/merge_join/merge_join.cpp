#include "duckdb/execution/merge_join.hpp"

#include "duckdb/parser/expression/comparison_expression.hpp"

using namespace std;

namespace duckdb {

template <class MJ, class L_ARG, class R_ARG> static idx_t merge_join(L_ARG &l, R_ARG &r) {
	switch (l.type.InternalType()) {
	case PhysicalType::BOOL:
	case PhysicalType::INT8:
		return MJ::template Operation<int8_t>(l, r);
	case PhysicalType::INT16:
		return MJ::template Operation<int16_t>(l, r);
	case PhysicalType::INT32:
		return MJ::template Operation<int32_t>(l, r);
	case PhysicalType::INT64:
		return MJ::template Operation<int64_t>(l, r);
	case PhysicalType::INT128:
		return MJ::template Operation<hugeint_t>(l, r);
	case PhysicalType::FLOAT:
		return MJ::template Operation<float>(l, r);
	case PhysicalType::DOUBLE:
		return MJ::template Operation<double>(l, r);
	case PhysicalType::INTERVAL:
		return MJ::template Operation<interval_t>(l, r);
	case PhysicalType::VARCHAR:
		return MJ::template Operation<string_t>(l, r);
	default:
		throw NotImplementedException("Type not implemented for merge join!");
	}
}

template <class T, class L_ARG, class R_ARG>
static idx_t perform_merge_join(L_ARG &l, R_ARG &r, ExpressionType comparison_type) {
	switch (comparison_type) {
	case ExpressionType::COMPARE_LESSTHAN:
		return merge_join<typename T::LessThan, L_ARG, R_ARG>(l, r);
	case ExpressionType::COMPARE_LESSTHANOREQUALTO:
		return merge_join<typename T::LessThanEquals, L_ARG, R_ARG>(l, r);
	case ExpressionType::COMPARE_GREATERTHAN:
		return merge_join<typename T::GreaterThan, L_ARG, R_ARG>(l, r);
	case ExpressionType::COMPARE_GREATERTHANOREQUALTO:
		return merge_join<typename T::GreaterThanEquals, L_ARG, R_ARG>(l, r);
	default:
		throw NotImplementedException("Unimplemented comparison type for merge join!");
	}
}

idx_t MergeJoinComplex::Perform(MergeInfo &l, MergeInfo &r, ExpressionType comparison_type) {
	assert(l.info_type == MergeInfoType::SCALAR_MERGE_INFO && r.info_type == MergeInfoType::SCALAR_MERGE_INFO);
	auto &left = (ScalarMergeInfo &)l;
	auto &right = (ScalarMergeInfo &)r;
	assert(left.type == right.type);
	if (left.order.count == 0 || right.order.count == 0) {
		return 0;
	}
	return perform_merge_join<MergeJoinComplex, ScalarMergeInfo, ScalarMergeInfo>(left, right, comparison_type);
}

idx_t MergeJoinSimple::Perform(MergeInfo &l, MergeInfo &r, ExpressionType comparison_type) {
	assert(l.info_type == MergeInfoType::SCALAR_MERGE_INFO && r.info_type == MergeInfoType::CHUNK_MERGE_INFO);
	auto &left = (ScalarMergeInfo &)l;
	auto &right = (ChunkMergeInfo &)r;
	assert(left.type == right.type);
	if (left.order.count == 0 || right.data_chunks.count == 0) {
		return 0;
	}
	return perform_merge_join<MergeJoinSimple, ScalarMergeInfo, ChunkMergeInfo>(left, right, comparison_type);
}

} // namespace duckdb
