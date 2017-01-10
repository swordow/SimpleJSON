/*
** created by swordow 01/26/2016
*/

#include "ccjson.h"
#include <typeinfo>
#include <math.h>

//
JSONString::JSONString(const char* istr) {
    val = std::string(istr);
}

//
JSONObject::JSONObject() :len(0) {
}
void JSONObject::addKeyValue(JSONString* key, JSONValue* val) {
    key_val.insert(std::make_pair(key->val, val));
	len++;
}

bool JSONObject::getString(const char* key, char*buffer, int *len) {
    std::map<std::string, JSONValue*>::iterator it = key_val.find(std::string(key));
    if (it == key_val.end()) return false;
    const char* val = dynamic_cast<JSONString*>(it->second)->val.c_str();
    int need_len = strlen(val);
    if (need_len >= *len) {
        *len = need_len+1;
        return false;
    }
    strncpy(buffer, val, (need_len + 1)*sizeof(char));
    *len = need_len + 1;
    return true;
}

bool JSONObject::getString(const char* key, std::string& val)
{
	std::map<std::string, JSONValue*>::iterator it = key_val.find(std::string(key));
    if (it == key_val.end()) return false;
    val = dynamic_cast<JSONString*>(it->second)->val;
    return true;
}

bool JSONObject::getNumber(const char* key, double* val) {
    std::map<std::string, JSONValue*>::iterator it = key_val.find(std::string(key));
    if (it == key_val.end()) return false;
    *val = dynamic_cast<JSONNumber*>(it->second)->val;
    return true;
}

bool JSONObject::getNumber(const char* key, float* val) {
	double x;
	if (!getNumber(key, &x))
	{
		return false;
	}
	
	*val = static_cast<float>(x);
    return true;
}
bool JSONObject::getNumber(const char* key, int* val) {
    double x;
	if (!getNumber(key, &x))
	{
		return false;
	}
	*val = static_cast<int>(x);
    return true;
}

bool JSONObject::getBool(const char* key, bool* val) {
    std::map<std::string, JSONValue*>::iterator it = key_val.find(std::string(key));
    if (it == key_val.end()) return false;
    *val = dynamic_cast<JSONBool*>(it->second)->val;
    return true;
}

bool JSONObject::getArray(const char* key, JSONArray** ja) {
    std::map<std::string, JSONValue*>::iterator it = key_val.find(std::string(key));
    if (it == key_val.end()) return false;
    *ja = dynamic_cast<JSONArray*>(it->second);
    return true;
}

bool JSONObject::getObject(const char* key, JSONObject** joo) {
    std::map<std::string, JSONValue*>::iterator it = key_val.find(std::string(key));
    if (it == key_val.end()) return false;
    *joo = dynamic_cast<JSONObject*>(it->second);
    return true;
}

//
JSONNumber::JSONNumber(double a) :val(a) {} 

//
JSONBool::JSONBool(bool a) :val(a){}

//
JSONArray::JSONArray(int size){
    jvs.clear();
    jvs.resize(size);
    len = 0;
}

void JSONArray::addJSONValue(JSONValue* jv) {
    if (len >= jvs.size()) {
        jvs.resize(len * 2);
    }
    jvs[len++] = jv; 
}
const JSONValue** JSONArray::getJSONValues() {
    return (const JSONValue**)(&jvs[0]);
}

const JSONValue* JSONArray::getJSONValueByIndex(int index)
{
    return jvs[index];
}

//
class JSONError
{
public:
	JSONError(const char* str, int error_index){
		char e[MAX_STR_SIZE] = {0};
		memcpy(e, str, error_index*sizeof(char));
		e[error_index] = '^';
		printf("Error Syntax (%d): %s\n", error_index, e);
	}
};

//
JSON::JSON(const char* str){
	json = 0;
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
			return 0;
		}
			
		//
		if (str[index] == '\'' || str[index] == '\"')
			key = decodeString();
		else {
			return 0;
		}
		
		if (key == 0) {
			return 0;
		}
		//
		index = passWhiteSpace();
		if (str[index] == ':') index++;
		else {
			return 0;
		}

		//
		index = passWhiteSpace();
		val = decodeValue();
		if (val == 0) {
			return 0;
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
			return 0;
		}
		JSONValue* res = decodeValue();
		if (res == 0) {
			return 0;
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

	return 0;
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
			return 0;
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
			return 0;
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
	return 0;
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
	return 0;
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
	
	if (json == 0) {
		JSONError je(str, index);
	}
}

void JSON::dumpNumber(JSONNumber* jn, char* buff, int* index)
{
    sprintf(&buff[*index], "%.4f", jn->val);
    (*index) += (strlen(&buff[*index]));
}

void JSON::dumpString(JSONString* js, char* buff, int* index)
{
	strcat(&buff[*index], "\'");
	strcat(&buff[*index], js->val.c_str());
	strcat(&buff[*index], "\'");
    (*index) += (strlen(&buff[*index]));
}

void JSON::dumpBool(JSONBool* jb, char* buff, int* index) {
	if (jb->val) {
		strcat(&buff[*index], "true");
	}else{
		strcat(&buff[*index], "false");
	}
    (*index) += (strlen(&buff[*index]));
}

void JSON::dumpNull(JSONNull* jn, char* buff, int* index) {
	strcat(&buff[*index], "null");
    (*index) += (strlen(&buff[*index]));
}

void JSON::dumpArray(JSONArray* ja, char* buff, int* index) {
	strcat(&buff[*index], "[");
    (*index) += 1;
	for (int i = 0; i < ja->len; i++) {
		dumpValue(ja->jvs[i], buff, index);
        strcat(&buff[*index], ",");
        (*index) += 1;
	}
	strcat(&buff[*index], "]");
    (*index) += 1;
}

void JSON::dumpObject(JSONObject* jo, char*buff, int* index){
    strcat(&buff[*index], "{");
    (*index) += 1;
    std::map<std::string, JSONValue*>::iterator it = jo->key_val.begin();
    for (; it != jo->key_val.end(); it++) {
        strcat(&buff[*index], "'");
        (*index) += 1;
        strcat(&buff[*index], it->first.c_str());
        (*index) += it->first.length();
        strcat(&buff[*index], "':");
        (*index) += 2;
		dumpValue(it->second, buff, index);
        strcat(&buff[*index], ",");
        (*index) += 1;
	}
    strcat(&buff[*index], "}");
    (*index) += 1;
}

void JSON::dumpValue(JSONValue* jv, char* buff,  int* index){
	if (dynamic_cast<JSONBool*>(jv) != 0) {
		dumpBool(static_cast<JSONBool*>(jv), buff, index);
		return;
	}
	if (dynamic_cast<JSONArray*>(jv) != 0) {
		dumpArray(static_cast<JSONArray*>(jv), buff, index);
		return;
	}
	if (dynamic_cast<JSONString*>(jv) != 0) {
		dumpString(static_cast<JSONString*>(jv), buff, index);
		return;
	}
	if (dynamic_cast<JSONNumber*>(jv) != 0) {
		dumpNumber(static_cast<JSONNumber*>(jv), buff, index);
		return;
	}
	if (dynamic_cast<JSONNull*>(jv) != 0) {
		dumpNull(static_cast<JSONNull*>(jv), buff, index);
		return;
	}
	if (dynamic_cast<JSONObject*>(jv) != 0) {
		dumpObject(static_cast<JSONObject*>(jv), buff, index);
		return;
	}
}

const char* JSON::dump(char*json_str){
    int i = 0;
	dumpValue(json, json_str, &i);
	return json_str;
}

bool JSON::getString(const char* key, char*buffer, int *len) {
	if (dynamic_cast<JSONObject*>(json) == 0) return false;
	JSONObject* jo = dynamic_cast<JSONObject*>(json);
    return jo->getString(key, buffer, len);
}

bool JSON::getString(const char* key, std::string& val) {
	if (dynamic_cast<JSONObject*>(json) == 0) return false;
	JSONObject* jo = dynamic_cast<JSONObject*>(json);
    return jo->getString(key, val);
}

bool JSON::getNumber(const char* key, double* val) {
	if (dynamic_cast<JSONObject*>(json) == 0) return false;
	JSONObject* jo = dynamic_cast<JSONObject*>(json);
    return jo->getNumber(key, val);
}

bool JSON::getNumber(const char* key, float* val) {
	if (dynamic_cast<JSONObject*>(json) == 0) return false;
	JSONObject* jo = dynamic_cast<JSONObject*>(json);
    return jo->getNumber(key, val);
}

bool JSON::getNumber(const char* key, int* val) {
	if (dynamic_cast<JSONObject*>(json) == 0) return false;
	JSONObject* jo = dynamic_cast<JSONObject*>(json);
    return jo->getNumber(key, val);
}

bool JSON::getBool(const char* key, bool* val) {
	if (dynamic_cast<JSONObject*>(json) == 0) return false;
	JSONObject* jo = dynamic_cast<JSONObject*>(json);
    return jo->getBool(key, val);
}

bool JSON::getArray(const char* key, JSONArray** ja) {
    if (dynamic_cast<JSONObject*>(json) == 0) return false;
    JSONObject* jo = dynamic_cast<JSONObject*>(json);
    return jo->getArray(key, ja);
}

bool JSON::getObject(const char* key, JSONObject** joo) {
    if (dynamic_cast<JSONObject*>(json) == 0) return false;
    JSONObject* jo = dynamic_cast<JSONObject*>(json);
    return jo->getObject(key, joo);
}

const JSONValue* JSON::getRootJSONValue() {
    return json;
}
