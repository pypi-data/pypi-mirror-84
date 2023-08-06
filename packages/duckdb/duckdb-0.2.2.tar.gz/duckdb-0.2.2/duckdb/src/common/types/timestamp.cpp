#include "duckdb/common/types/timestamp.hpp"

#include "duckdb/common/exception.hpp"
#include "duckdb/common/types/date.hpp"
#include "duckdb/common/types/time.hpp"
#include "duckdb/common/string_util.hpp"

#include <chrono> // chrono::system_clock
#include <ctime>

using namespace std;

namespace duckdb {

// timestamp/datetime uses 64 bits, high 32 bits for date and low 32 bits for time
// string format is YYYY-MM-DDThh:mm:ssZ
// T may be a space
// Z is optional
// ISO 8601

timestamp_t Timestamp::FromCString(const char *str, idx_t len) {
	idx_t pos;
	date_t date;
	dtime_t time;
	if (!Date::TryConvertDate(str, pos, date)) {
		throw ConversionException("timestamp field value out of range: \"%s\", "
		                          "expected format is (YYYY-MM-DD HH:MM:SS[.MS])",
		                          str);
	}
	if (pos == len) {
		// no time: only a date
		return (uint64_t)date << 32;
	}
	// try to parse a time field
	if (str[pos] == ' ' || str[pos] == 'T') {
		pos++;
	}
	idx_t time_pos = 0;
	if (!Time::TryConvertTime(str + pos, time_pos, time)) {
		throw ConversionException("timestamp field value out of range: \"%s\", "
		                          "expected format is (YYYY-MM-DD HH:MM:SS[.MS])",
		                          str);
	}
	pos += time_pos;
	if (pos < len) {
		// skip a "Z" at the end (as per the ISO8601 specs)
		if (str[pos] == 'Z') {
			pos++;
		}
		// skip any spaces at the end
		while (pos < len && StringUtil::CharacterIsSpace(str[pos])) {
			pos++;
		}
		if (pos < len) {
			throw ConversionException("timestamp field value out of range: \"%s\", "
			                          "expected format is (YYYY-MM-DD HH:MM:SS[.MS])",
			                          str);
		}
	}
	// use uint here because otherwise the shift is undefined
	return ((uint64_t)date << 32 | (int32_t)time);
}

timestamp_t Timestamp::FromString(string str) {
	return Timestamp::FromCString(str.c_str(), str.size());
}

string Timestamp::ToString(timestamp_t timestamp) {
	return Date::ToString(GetDate(timestamp)) + " " + Time::ToString(GetTime(timestamp));
}

date_t Timestamp::GetDate(timestamp_t timestamp) {
	return (date_t)(((uint64_t)timestamp) >> 32);
}

dtime_t Timestamp::GetTime(timestamp_t timestamp) {
	return (dtime_t)(timestamp & 0xFFFFFFFF);
}

timestamp_t Timestamp::FromDatetime(date_t date, dtime_t time) {
	return ((uint64_t)date << 32 | (int64_t)time);
}

void Timestamp::Convert(timestamp_t date, date_t &out_date, dtime_t &out_time) {
	out_date = GetDate(date);
	out_time = GetTime(date);
}

timestamp_t Timestamp::GetCurrentTimestamp() {
	using std::chrono::system_clock;
	auto now = std::chrono::system_clock::now();
	auto epoch_ms = std::chrono::duration_cast<std::chrono::milliseconds>(now.time_since_epoch()).count();
	return Timestamp::FromEpochMs(epoch_ms);
}

timestamp_t Timestamp::FromEpochMs(int64_t ms) {
	auto ms_per_day = (int64_t)60 * 60 * 24 * 1000;
	date_t date = Date::EpochToDate(ms / 1000);
	dtime_t time = (dtime_t)(ms % ms_per_day);
	return Timestamp::FromDatetime(date, time);
}

timestamp_t Timestamp::FromEpochMicroSeconds(int64_t micros) {
	return Timestamp::FromEpochMs(micros / 1000);
}

int64_t Timestamp::GetEpoch(timestamp_t timestamp) {
	return Date::Epoch(Timestamp::GetDate(timestamp)) + (int64_t)(Timestamp::GetTime(timestamp) / 1000);
}

int64_t Timestamp::GetMilliseconds(timestamp_t timestamp) {
	int n = Timestamp::GetTime(timestamp);
	int m = n / 60000;
	return n - m * 60000;
}

int64_t Timestamp::GetSeconds(timestamp_t timestamp) {
	int n = Timestamp::GetTime(timestamp);
	int m = n / 60000;
	return (n - m * 60000) / 1000;
}

int64_t Timestamp::GetMinutes(timestamp_t timestamp) {
	int n = Timestamp::GetTime(timestamp);
	int h = n / 3600000;
	return (n - h * 3600000) / 60000;
}

int64_t Timestamp::GetHours(timestamp_t timestamp) {
	return Timestamp::GetTime(timestamp) / 3600000;
}

} // namespace duckdb
