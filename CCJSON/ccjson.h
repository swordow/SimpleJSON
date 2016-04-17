/*
** created by swordow on 01/26/2016
*/

#ifndef __CC_JSON_H__
#define __CC_JSON_H__

#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#define MAX_ARRAY_SIZE  10240	
#define MAX_STR_SIZE	256

class JSONValue{
public:
	JSONValue(){}
	virtual ~JSONValue(){};
};

class JSONString : public JSONValue{
public:
	JSONString(const char* istr);
	char val[MAX_STR_SIZE];
};

class JSONObject : public JSONValue{
public:
	JSONObject();
	void addKeyValue(JSONString* key, JSONValue* val);
	JSONString** keys;
	JSONValue** vals;
	int len;
};

class JSONNumber : public JSONValue{
public:
	JSONNumber(double a);
	double val;
};

class JSONBool : public JSONValue{
public:
	JSONBool(bool a);
	bool val;
};

class JSONNull : public JSONValue{};

class JSONArray : public JSONValue{
public:
	void addJSONValue(JSONValue* jv);
	JSONArray(int size=MAX_ARRAY_SIZE);
	int len;
	JSONValue** jvs;
};

class JSON {
public:
	JSON(const char* str);
	~JSON();
	//
	JSONString* decodeString();
	JSONObject* decodeObject();
	JSONArray* decodeArray();
	JSONBool* decodeBool();
	JSONNumber* decodeNumber();
	JSONNull* decodeNull();
	JSONValue* decodeValue();
	inline bool isWhiteSpace(char c);
	inline bool isDigital(char c);
	inline int passWhiteSpace();
	void decode(const char* json_str);

	//
	void dumpNumber(JSONNumber* jn, char* buff, int* index);
	void dumpString(JSONString* js, char* buff, int* index);
	void dumpBool(JSONBool* jb, char* buff, int* index);
	void dumpNull(JSONNull* jn, char* buff, int* index);
	void dumpArray(JSONArray* ja, char*buff, int* index);
	void dumpObject(JSONObject* jo, char*buff, int* index);
	void dumpValue(JSONValue* jv, char* buff, int* index);
	const char* dump(char* json_str);
	
	//
	bool getString(const char*key, char*buff, int* len);
	bool getNumber(const char* key, double* val);
	bool getBool(const char* key, bool* val);
	
	JSONValue* json;
	const char* str;
	int index;
};
#endif // __CC_JSON_H__
