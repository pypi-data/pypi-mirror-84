#include "duckdb/function/aggregate/distributive_functions.hpp"
#include "duckdb/common/exception.hpp"
#include "duckdb/common/types/null_value.hpp"
#include "duckdb/common/vector_operations/vector_operations.hpp"
#include "duckdb/common/algorithm.hpp"

using namespace std;

namespace duckdb {

struct string_agg_state_t {
	idx_t size;
	idx_t alloc_size;
	char *dataptr;
};

struct StringAggBaseFunction {
	template <class STATE> static void Initialize(STATE *state) {
		state->dataptr = nullptr;
		state->alloc_size = 0;
		state->size = 0;
	}

	template <class T, class STATE>
	static void Finalize(Vector &result, STATE *state, T *target, nullmask_t &nullmask, idx_t idx) {
		if (!state->dataptr) {
			nullmask[idx] = true;
		} else {
			target[idx] = StringVector::AddString(result, state->dataptr, state->size);
		}
	}

	template <class STATE> static void Destroy(STATE *state) {
		if (state->dataptr) {
			delete[] state->dataptr;
		}
	}

	static bool IgnoreNull() {
		return true;
	}

	static inline void PerformOperation(string_agg_state_t *state, const char *str, const char *sep, idx_t str_size,
	                                    idx_t sep_size) {
		if (state->dataptr == nullptr) {
			// first iteration: allocate space for the string and copy it into the state
			state->alloc_size = MaxValue<idx_t>(8, NextPowerOfTwo(str_size));
			state->dataptr = new char[state->alloc_size];
			state->size = str_size - 1;
			memcpy(state->dataptr, str, str_size);
		} else {
			// subsequent iteration: first check if we have space to place the string and separator
			idx_t required_size = state->size + str_size + sep_size;
			if (required_size > state->alloc_size) {
				// no space! allocate extra space
				while (state->alloc_size < required_size) {
					state->alloc_size *= 2;
				}
				auto new_data = new char[state->alloc_size];
				memcpy(new_data, state->dataptr, state->size);
				delete[] state->dataptr;
				state->dataptr = new_data;
			}
			// copy the separator
			memcpy(state->dataptr + state->size, sep, sep_size);
			state->size += sep_size;
			// copy the string
			memcpy(state->dataptr + state->size, str, str_size);
			state->size += str_size - 1;
		}
	}

	static inline void PerformOperation(string_agg_state_t *state, string_t str, string_t sep) {
		PerformOperation(state, str.GetData(), sep.GetData(), str.GetSize() + 1, sep.GetSize());
	}

	static inline void PerformOperation(string_agg_state_t *state, string_t str) {
		PerformOperation(state, str.GetData(), ",", str.GetSize() + 1, 1);
	}
};

struct StringAggFunction : public StringAggBaseFunction {
	template <class A_TYPE, class B_TYPE, class STATE, class OP>
	static void Operation(STATE *state, A_TYPE *str_data, B_TYPE *sep_data, nullmask_t &str_nullmask,
	                      nullmask_t &sep_nullmask, idx_t str_idx, idx_t sep_idx) {
		PerformOperation(state, str_data[str_idx], sep_data[sep_idx]);
	}
};

struct StringAggSingleFunction : public StringAggBaseFunction {
	template <class INPUT_TYPE, class STATE, class OP>
	static void Operation(STATE *state, INPUT_TYPE *str_data, nullmask_t &str_nullmask, idx_t str_idx) {
		PerformOperation(state, str_data[str_idx]);
	}

	template <class INPUT_TYPE, class STATE, class OP>
	static void ConstantOperation(STATE *state, INPUT_TYPE *input, nullmask_t &nullmask, idx_t count) {
		for (idx_t i = 0; i < count; i++) {
			Operation<INPUT_TYPE, STATE, OP>(state, input, nullmask, 0);
		}
	}

	template <class STATE, class OP> static void Combine(STATE source, STATE *target) {
		if (source.dataptr == nullptr) {
			// source is not set: skip combining
			return;
		}
		PerformOperation(target, string_t(source.dataptr, source.size));
		Destroy(&source);
	}
};

void StringAggFun::RegisterFunction(BuiltinFunctions &set) {
	AggregateFunctionSet string_agg("string_agg");
	string_agg.AddFunction(AggregateFunction(
	    {LogicalType::VARCHAR, LogicalType::VARCHAR}, LogicalType::VARCHAR,
	    AggregateFunction::StateSize<string_agg_state_t>,
	    AggregateFunction::StateInitialize<string_agg_state_t, StringAggFunction>,
	    AggregateFunction::BinaryScatterUpdate<string_agg_state_t, string_t, string_t, StringAggFunction>, nullptr,
	    AggregateFunction::StateFinalize<string_agg_state_t, string_t, StringAggFunction>,
	    AggregateFunction::BinaryUpdate<string_agg_state_t, string_t, string_t, StringAggFunction>, nullptr,
	    AggregateFunction::StateDestroy<string_agg_state_t, StringAggFunction>));
	string_agg.AddFunction(AggregateFunction(
	    {LogicalType::VARCHAR}, LogicalType::VARCHAR, AggregateFunction::StateSize<string_agg_state_t>,
	    AggregateFunction::StateInitialize<string_agg_state_t, StringAggSingleFunction>,
	    AggregateFunction::UnaryScatterUpdate<string_agg_state_t, string_t, StringAggSingleFunction>,
	    AggregateFunction::StateCombine<string_agg_state_t, StringAggSingleFunction>,
	    AggregateFunction::StateFinalize<string_agg_state_t, string_t, StringAggSingleFunction>,
	    AggregateFunction::UnaryUpdate<string_agg_state_t, string_t, StringAggSingleFunction>, nullptr,
	    AggregateFunction::StateDestroy<string_agg_state_t, StringAggSingleFunction>));
	set.AddFunction(string_agg);
	string_agg.name = "group_concat";
	set.AddFunction(string_agg);
}

} // namespace duckdb
