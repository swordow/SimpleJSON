/*
** created by swordow 01/26/2016
*/

#include "ccjson.h"
#include <typeinfo>
//
JSONString::JSONString(const char* istr) {
	memcpy(val, istr, (strlen(istr) + 1)*sizeof(char));
}

//
JSONObject::JSONObject() :len(0) {
	keys = new JSONString*[MAX_ARRAY_SIZE];
	vals = new JSONValue*[MAX_ARRAY_SIZE];
}
void JSONObject::addKeyValue(JSONString* key, JSONValue* val) {
	keys[len] = key;
	vals[len] = val;
	len++;
}

//
JSONNumber::JSONNumber(double a) :val(a) {} 

//
JSONBool::JSONBool(bool a) :val(a){}

//
JSONArray::JSONArray():len(0){ jvs = new JSONValue*[MAX_ARRAY_SIZE]; }
void JSONArray::addJSONValue(JSONValue* jv) { jvs[len++] = jv; }

//
class JSONError
{
public:
	JSONError(const char* str, int error_index){
		char e[MAX_STR_SIZE] = {0};
		memcpy(e, str, error_index*sizeof(char));
		e[error_index] = '^';
		printf("Error Syntax: %s\n", e);
	}
};

//
JSON::JSON(const char* str){
	json = nullptr;
	decode(str);
}

JSON::~JSON(){
	delete json;
}

JSONString* JSON::decodeString()
{
	char ss = str[index];
	index++;
	int si = index;
	while (str[index] != ss && str[index-1]!='\\') index++;
	char v[MAX_STR_SIZE] = { 0 };
	memcpy(v, &str[si], (index - si)*sizeof(char));
	index++;
	return new JSONString(v);
}

JSONObject* JSON::decodeObject()
{
	index++;
	bool fin = false;
	JSONObject* jo = new JSONObject();
	while (true) {
		JSONString* key;
		JSONValue* val;
		index = passWhiteSpace();
			
		//
		if (str[index] == '}')  {
			index++;
			return jo;
		} else if (fin) {
			return nullptr;
		}
			
		//
		if (str[index] == '\'' || str[index] == '\"')
			key = decodeString();
		else {
			return nullptr;
		}
		
		if (key == nullptr) {
			return nullptr;
		}
		//
		index = passWhiteSpace();
		if (str[index] == ':') index++;
		else {
			return nullptr;
		}

		//
		index = passWhiteSpace();
		val = decodeValue();
		if (val == nullptr) {
			return nullptr;
		}

		jo->addKeyValue(key, val);
		//
		index = passWhiteSpace();
		if (str[index] == ',') index++;
		else fin = true;
	}
}

JSONArray* JSON::decodeArray()
{
	index++;
	bool fin = false;
	JSONArray* ja = new JSONArray();
	while (true) {
		index = passWhiteSpace();
		if (str[index] == ']') {
			index++;
			return ja;
		} else if (fin) {
			return nullptr;
		}
		JSONValue* res = decodeValue();
		if (res == nullptr) {
			return nullptr;
		}
		ja->addJSONValue(res);
		if (str[index] == ',') index++;
		else fin=true;
	}
}

JSONBool* JSON::decodeBool()
{
	if (str[index] == 'f' &&
		str[index+1] == 'a' &&
		str[index+2] == 'l' &&
		str[index+3] == 's' &&
		str[index+4] == 'e') {
		index += 5;
		return new JSONBool(false);
	}

	if (str[index] == 't' &&
		str[index+1] == 'r' &&
		str[index+2] == 'u' &&
		str[index+3] == 'e') {
		index += 4;
		return new JSONBool(true);
	}

	return nullptr;
}

JSONNumber* JSON::decodeNumber()
{
	int start_index = index;
	if (str[index] == '0') index++;
	else if (str[index] == '-'){
		if (str[index + 1] == '0') index += 2;
		else if (isDigital(str[index + 1])) {
			index += 2;
			while (isDigital(str[index])) index++;
		}
		else {
			return nullptr;
		}
	}else while (isDigital(str[index])) index++;

	if (str[index] == '.'){
		index++;
		while (isDigital(str[index])) index++;
	}

	if (str[index] == 'e' || str[index] == 'E'){
		index++;
		if (str[index] == '+' || str[index] == '-') index++;
		if (isDigital(str[index])) while (isDigital(str[index])) index++;
		else{
			return nullptr;
		}
	}
	char v[MAX_STR_SIZE] = { 0 };
	memcpy(v, &str[start_index], (index - start_index)*sizeof(char));
	return new JSONNumber(atof(v));
}

JSONNull* JSON::decodeNull()
{
	if (str[index] == 'n' &&
		str[index + 1] == 'u' &&
		str[index + 2] == 'l' &&
		str[index + 3] == 'l') {
		index += 4;
		return new JSONNull();
	}
	return nullptr;
}

JSONValue* JSON::decodeValue()
{
	if (str[index] == '\'' || str[index]=='\"')
		return decodeString();
		
	if (str[index] == '{')
		return decodeObject();
		
	if (str[index] == '[')
		return decodeArray();
		
	if (str[index] == '-' || isDigital(str[index]))
		return decodeNumber();
		
	if (str[index] == 'f' || str[index] == 't') 
		return decodeBool();

	if (str[index] == 'n')
		return decodeNull();

	JSONError je(str,index);
	return nullptr;
}

inline bool JSON::isWhiteSpace(char c) {
	if (c == ' ' || c == '\t' || c == '\r' || c == '\n')
		return true;
	return false;
}

inline bool JSON::isDigital(char c) {
	int x = c-'0';
	if (x  >= 0 && x <= 9) return true;
	return false;
}

inline int JSON::passWhiteSpace()
{
	while (isWhiteSpace(str[index])) index++;
	return index;
}

void JSON::decode(const char* json_str){
	str = json_str;
	index = 0;
	index = passWhiteSpace();
	if (str[index] == '{') 
		json = decodeObject();
	else if (str[index] == '[')
		json = decodeArray();
	
	if (json == nullptr) {
		JSONError je(str, index);
	}
}

void JSON::dumpNumber(JSONNumber* jn, char* buff)
{
	sprintf(&buff[strlen(buff)], "%f", jn->val);
}

void JSON::dumpString(JSONString* js, char* buff)
{
	strcat(buff, "\'");
	strcat(buff, js->val);
	strcat(buff, "\'");
}

void JSON::dumpBool(JSONBool* jb, char* buff) {
	if (jb->val) {
		strcat(buff, "true");
	}else{
		strcat(buff, "false");
	}
}

void JSON::dumpNull(JSONNull* jn, char* buff) {
	strcat(buff, "null");
}

void JSON::dumpArray(JSONArray* ja, char*buff){
	strcat(buff, "[");
	for (int i = 0; i < ja->len; i++) {
		dumpValue(ja->jvs[i], buff);
		strcat(buff, ",");
	}
	strcat(buff, "]");
}

void JSON::dumpObject(JSONObject* jo, char*buff) {
	strcat(buff, "{");
	for (int i = 0; i < jo->len; i++) {
		dumpString(jo->keys[i], buff);
		strcat(buff, ":");
		dumpValue(jo->vals[i], buff);
		strcat(buff, ",");
	}
	strcat(buff, "}");
}

void JSON::dumpValue(JSONValue* jv, char* buff){
	if (dynamic_cast<JSONBool*>(jv) != nullptr) {
		dumpBool(static_cast<JSONBool*>(jv), buff);
		return;
	}
	if (dynamic_cast<JSONArray*>(jv) != nullptr) {
		dumpArray(static_cast<JSONArray*>(jv), buff);
		return;
	}
	if (dynamic_cast<JSONString*>(jv) != nullptr) {
		dumpString(static_cast<JSONString*>(jv), buff);
		return;
	}
	if (dynamic_cast<JSONNumber*>(jv) != nullptr) {
		dumpNumber(static_cast<JSONNumber*>(jv), buff);
		return;
	}
	if (dynamic_cast<JSONNull*>(jv) != nullptr) {
		dumpNull(static_cast<JSONNull*>(jv), buff);
		return;
	}
	if (dynamic_cast<JSONObject*>(jv) != nullptr) {
		dumpObject(static_cast<JSONObject*>(jv), buff);
		return;
	}
}

const char* JSON::dump(char*json_str){
	dumpValue(json, json_str);
	return json_str;
}

bool JSON::getString(const char* key, char*buffer, int *len) {
	if (dynamic_cast<JSONObject*>(json) == nullptr) return false;
	JSONObject* jo = dynamic_cast<JSONObject*>(json);
	for (int i = 0; i < jo->len; i++) {
		if (strcmp(key, jo->keys[i]->val) == 0){
			const char* val = dynamic_cast<JSONString*>(jo->vals[i])->val;
			strncpy(buffer, val, (strlen(val) + 1)*sizeof(char));
			return true;
		}
	}
	return false;
}

bool JSON::getNumber(const char* key, double* val) {
	if (dynamic_cast<JSONObject*>(json) == nullptr) return false;
	JSONObject* jo = dynamic_cast<JSONObject*>(json);
	for (int i = 0; i < jo->len; i++) {
		if (strcmp(key, jo->keys[i]->val) == 0){
			*val = dynamic_cast<JSONNumber*>(jo->vals[i])->val;
			return true;
		}
	}
	return false;
}

bool JSON::getBool(const char* key, bool* val) {
	if (dynamic_cast<JSONObject*>(json) == nullptr) return false;
	JSONObject* jo = dynamic_cast<JSONObject*>(json);
	for (int i = 0; i < jo->len; i++) {
		if (strcmp(key, jo->keys[i]->val) == 0){
			*val = dynamic_cast<JSONBool*>(jo->vals[i])->val;
			return true;
		}
	}
	return false;
}
