//===----------------------------------------------------------------------===//
//                         DuckDB
//
// duckdb/common/operator/comparison_operators.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "duckdb/common/types/string_type.hpp"
#include "duckdb/common/types.hpp"
#include "duckdb/common/types/hugeint.hpp"
#include "duckdb/common/types/interval.hpp"

#include <cstring>

namespace duckdb {

//===--------------------------------------------------------------------===//
// Comparison Operations
//===--------------------------------------------------------------------===//
struct Equals {
	template <class T> static inline bool Operation(T left, T right) {
		return left == right;
	}
};
struct NotEquals {
	template <class T> static inline bool Operation(T left, T right) {
		return left != right;
	}
};
struct GreaterThan {
	template <class T> static inline bool Operation(T left, T right) {
		return left > right;
	}
};
struct GreaterThanEquals {
	template <class T> static inline bool Operation(T left, T right) {
		return left >= right;
	}
};
struct LessThan {
	template <class T> static inline bool Operation(T left, T right) {
		return left < right;
	}
};
struct LessThanEquals {
	template <class T> static inline bool Operation(T left, T right) {
		return left <= right;
	}
};
//===--------------------------------------------------------------------===//
// Specialized Boolean Comparison Operators
//===--------------------------------------------------------------------===//
template <> inline bool GreaterThan::Operation(bool left, bool right) {
	return !right && left;
}
template <> inline bool LessThan::Operation(bool left, bool right) {
	return !left && right;
}
//===--------------------------------------------------------------------===//
// Specialized String Comparison Operations
//===--------------------------------------------------------------------===//
struct StringComparisonOperators {
	template <bool INVERSE> static inline bool EqualsOrNot(const string_t a, const string_t b) {
		if (memcmp(&a, &b, sizeof(uint32_t) + string_t::PREFIX_LENGTH) == 0) {
			// prefix and length are equal
			if (a.IsInlined()) {
				// small string: compare entire inlined string
				if (memcmp(a.value.inlined.inlined, b.value.inlined.inlined, a.GetSize()) == 0) {
					// entire string is equal
					return INVERSE ? false : true;
				}
			} else {
				// large string: check main data source
				if (memcmp(a.value.pointer.ptr, b.value.pointer.ptr, a.GetSize()) == 0) {
					// entire string is equal
					return INVERSE ? false : true;
				}
			}
		}
		// not equal
		return INVERSE ? true : false;
	}
};
template <> inline bool Equals::Operation(string_t left, string_t right) {
	return StringComparisonOperators::EqualsOrNot<false>(left, right);
}
template <> inline bool NotEquals::Operation(string_t left, string_t right) {
	return StringComparisonOperators::EqualsOrNot<true>(left, right);
}
template <> inline bool GreaterThan::Operation(string_t left, string_t right) {
	return strcmp(left.GetData(), right.GetData()) > 0;
}
template <> inline bool GreaterThanEquals::Operation(string_t left, string_t right) {
	return strcmp(left.GetData(), right.GetData()) >= 0;
}
template <> inline bool LessThan::Operation(string_t left, string_t right) {
	return strcmp(left.GetData(), right.GetData()) < 0;
}
template <> inline bool LessThanEquals::Operation(string_t left, string_t right) {
	return strcmp(left.GetData(), right.GetData()) <= 0;
}
//===--------------------------------------------------------------------===//
// Specialized Interval Comparison Operators
//===--------------------------------------------------------------------===//
template <> inline bool Equals::Operation(interval_t left, interval_t right) {
	return Interval::Equals(left, right);
}
template <> inline bool NotEquals::Operation(interval_t left, interval_t right) {
	return !Equals::Operation(left, right);
}
template <> inline bool GreaterThan::Operation(interval_t left, interval_t right) {
	return Interval::GreaterThan(left, right);
}
template <> inline bool GreaterThanEquals::Operation(interval_t left, interval_t right) {
	return Interval::GreaterThanEquals(left, right);
}
template <> inline bool LessThan::Operation(interval_t left, interval_t right) {
	return GreaterThan::Operation(right, left);
}
template <> inline bool LessThanEquals::Operation(interval_t left, interval_t right) {
	return GreaterThanEquals::Operation(right, left);
}
//===--------------------------------------------------------------------===//
// Specialized Hugeint Comparison Operators
//===--------------------------------------------------------------------===//
template <> inline bool Equals::Operation(hugeint_t left, hugeint_t right) {
	return Hugeint::Equals(left, right);
}
template <> inline bool NotEquals::Operation(hugeint_t left, hugeint_t right) {
	return Hugeint::NotEquals(left, right);
}
template <> inline bool GreaterThan::Operation(hugeint_t left, hugeint_t right) {
	return Hugeint::GreaterThan(left, right);
}
template <> inline bool GreaterThanEquals::Operation(hugeint_t left, hugeint_t right) {
	return Hugeint::GreaterThanEquals(left, right);
}
template <> inline bool LessThan::Operation(hugeint_t left, hugeint_t right) {
	return Hugeint::LessThan(left, right);
}
template <> inline bool LessThanEquals::Operation(hugeint_t left, hugeint_t right) {
	return Hugeint::LessThanEquals(left, right);
}
} // namespace duckdb
