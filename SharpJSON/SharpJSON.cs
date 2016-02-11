/*
** created by swordow on 01/26/2016
*/

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SharpJSON
{
    public class SharpJSON
    {
        JSONValue json;
        class JSONError : Exception
        {
            public JSONError(string str, int index)
            {
                System.Console.Out.Write(str.Substring(0, index) + "^");
            }
        }
       
        public SharpJSON(string str)
        {
            decode(str);
        }

        public void get(string key_str, ref string val)
        {
            JSONObject obj = (JSONObject)json;
            val = ((JSONString)obj.get(new JSONString(key_str))).str;
            
        }
        public void get(string key_str, ref double val)
        {
            JSONObject obj = (JSONObject)json;
            val = ((JSONNumber)obj.get(new JSONString(key_str))).val;

        }
        public void get(string key_str, ref bool val)
        {
            JSONObject obj = (JSONObject)json;
            val = ((JSONBool)obj.get(new JSONString(key_str))).val;
        }
				
				public void get(string key_str, ref SharpJSON sj)
				{
            JSONObject obj = (JSONObject)json;
            JSONValue val = ((JSONObject)obj.get(new JSONString(key_str))).val;
						string str = "";
						if (val is JSONArray) str = dumpArray((JSONArray)val);
						if (val is JSONObject) str = dumpObject((JSONObject)val)
						sj = new SharpJSON(str);
				}

        public string dump()
        {
            string str = "";
            if (json is JSONArray)
            {
                str = dumpArray((JSONArray)json);
            }
            if (json is JSONObject)
            {
                str = dumpObject((JSONObject)json);
            }
            return str;
        }

        public string dumpArray(JSONArray json)
        {
            string str = "[";
            for (int i = 0; i < json.len; i++)
            {
                str += dumpValue(json.value[i]) + ",";
            }
            return str + "]";
        }

        public string dumpObject(JSONObject json)
        {
            string str = "{";
            for (int i = 0; i < json.len; i++)
            {
                str += "" + dumpValue(json.keys[i]) + ":" + dumpValue(json.vals[i]) + ",";
            }
            return str + "}";
        }

        public string dumpValue(JSONValue val)
        {
            if (val is JSONString)
            {
                return "\'" + ((JSONString)val).str + "\'";
            }
            if (val is JSONNull)
            {
                return "null";
            }
            if (val is JSONBool)
            {
                if (((JSONBool)val).val)
                {
                    return "true";
                }
                else
                {
                    return "false";
                }
            }
            if (val is JSONArray)
            {
                return dumpArray((JSONArray)val);
            }
            if (val is JSONObject)
            {
                return dumpObject((JSONObject)val);
            }

            if (val is JSONNumber)
            {
                return ((JSONNumber)val).val.ToString();
            }
            return "";
        }

        public class JSONValue
        {

        }

        public class JSONObject : JSONValue
        {
            public JSONString[] keys;
            public JSONValue[] vals;
            public int len;
            public JSONObject()
            {
                keys = new JSONString[1000];
                vals = new JSONValue[1000];
                len = 0;
            }
            public void addStringValue(JSONString key, JSONValue val)
            {
                keys[len] = key;
                vals[len] = val;
                len++;
            }
            public JSONValue get(JSONString key)
            {
                for (int i = 0; i < len; i++)
                {
                    if (key.str == keys[i].str)
                    {
                        return vals[i];
                    }
                }
                return null;
            }
        }

        public class JSONArray : JSONValue
        {
            public JSONValue[] value;
            public int len;
            public JSONArray()
            {
                value = new JSONValue[1000];
                len = 0;
            }
            public void addJSONValue(JSONValue obj) { value[len++] = obj; }
        }

        public class JSONString : JSONValue
        {
            public string str;
            public JSONString(string str)
            {
                this.str = str;
            }
        }

        public class JSONNumber : JSONValue
        {
            public double val;
            public JSONNumber(double a)
            {
                val = a;
            }
        }

        public class JSONNull : JSONValue { }

        public class JSONBool : JSONValue
        {
            public bool val;
            public JSONBool(bool x)
            {
                val = x;
            }
        }

        public JSONString decodeString(string str, ref int index)
        {
            char start_char = str[index];
            index++;
            int start_index = index;
            while (index < str.Length && str[index] != start_char && str[index - 1] != '\\')
            {
                index++;
            }
            index++;
            return new JSONString(str.Substring(start_index, index - start_index - 1));
        }

        public JSONNumber decodeNumber(string str, ref int index)
        {
            int start_index = index;
            if (str[index] == '0')
            {
                index++;

            }
            else if (str[index] == '-')
            {
                if (str[index + 1] == '0')
                {
                    index += 2;
                }
                else if (str[index + 1] - '0' >= 0 && str[index + 1] - '0' <= 9)
                {
                    index += 2;
                    while (str[index] - '0' >= 0 && str[index] - '0' <= 9)
                    {
                        index++;
                    }
                }
                else throw new JSONError(str, index);
            }
            else
            {
                while (str[index] - '0' >= 0 && str[index] - '0' <= 9)
                {
                    index++;
                }
            }

            if (str[index] == '.')
            {
                index++;
                while (str[index] - '0' >= 0 && str[index] - '0' <= 9)
                {
                    index++;
                }
            }

            if (str[index] == 'e' || str[index] == 'E')
            {
                index++;
                if (str[index] == '+' || str[index] == '-')
                {
                    index++;
                }
                if (str[index] - '0' >= 0 && str[index] - '0' <= 9)
                {
                    while (str[index] - '0' >= 0 && str[index] - '0' <= 9)
                    {
                        index++;
                    }
                }
                else
                {
                    throw new JSONError(str, index);
                }
            }
            return new JSONNumber(Convert.ToDouble(str.Substring(start_index, index - start_index)));
        }

        public JSONBool decodeBool(string str, ref int index)
        {
            if (str[index + 0] == 'f' &&
               str[index + 1] == 'a' &&
               str[index + 2] == 'l' &&
               str[index + 3] == 's' &&
               str[index + 4] == 'e')
            {
                index += 5;
                return new JSONBool(false);
            }
            if (str[index + 0] == 't' &&
               str[index + 1] == 'r' &&
               str[index + 2] == 'u' &&
               str[index + 3] == 'e')
            {
                index += 4;
                return new JSONBool(true);
            }
            throw new JSONError(str, index);
        }

        public JSONNull decodeNull(string str, ref int index)
        {
            if (str[index + 0] == 'n' &&
               str[index + 1] == 'u' &&
               str[index + 2] == 'l' &&
               str[index + 3] == 'l')
            {
                index += 4;
                return new JSONNull();
            }
            throw new JSONError(str, index);
        }

        public JSONValue decodeValue(string str, ref int index)
        {
            index = passWhiteSpace(str, index);
            if (str[index] == '{')
            {
                return decodeObject(str, ref index);
            }
            if (str[index] == '[')
            {
                return decodeArray(str, ref index);
            }
            if (str[index] == '\'' || str[index] == '\"')
            {
                return decodeString(str, ref index);
            }
            if (str[index] == 'f' || str[index] == 't')
            {
                return decodeBool(str, ref index);
            }
            if (str[index] == 'n')
            {
                return decodeNull(str, ref index);
            }
            if (str[index] == '-' || str[index] - '0' >= 0 && str[index] - '0' <= 9)
            {
                return decodeNumber(str, ref index);
            }
            throw new JSONError(str, index);
        }

        public JSONArray decodeArray(string str, ref int index)
        {
            if (str[index] != '[') return null;
            index++;
            JSONArray array = new JSONArray();
            bool array_should_over = false;
            while (index < str.Length)
            {
                index = passWhiteSpace(str, index);
                if (str[index] == ']')
                {
                    index++;
                    return array;
                }
                else if (array_should_over)
                {

                    throw new JSONError(str, index);
                }
                array.addJSONValue(decodeValue(str, ref index));
                index = passWhiteSpace(str, index);
                if (str[index] != ',')
                {
                    array_should_over = true;
                }
                else
                {
                    index++;
                }


            }

            return null;
        }
        public JSONObject decodeObject(string str, ref int index)
        {
            if (str[index] != '{') return null;
            index++;
            JSONObject jo = new JSONObject();
            bool object_should_over = false;
            while (index < str.Length)
            {
                JSONString key = null;
                JSONValue val = null;
                index = passWhiteSpace(str, index);

                if (str[index] == '}')
                {
                    index++;
                    return jo;
                }
                else if (object_should_over) throw new JSONError(str, index);

                if (str[index] == '\'' || str[index] == '\"')
                    key = decodeString(str, ref index);

                if (key == null) throw new JSONError(str, index);

                index = passWhiteSpace(str, index);

                if (str[index] != ':') throw new JSONError(str, index);
                index++;

                val = decodeValue(str, ref index);

                if (val == null) throw new JSONError(str, index);

                jo.addStringValue(key, val);

                index = passWhiteSpace(str, index);
                if (str[index] != ',')
                {
                    object_should_over = true;
                }
                else
                {
                    index++;
                }
            }
            return null;
        }

        public int passWhiteSpace(string str, int index)
        {
            for (int i = index; i < str.Length; i++)
            {
                if (str[i] == ' ' || str[i] == '\t' || str[i] == '\r' || str[i] == '\n')
                {
                    continue;
                }
                else
                {
                    return i;
                }
            }
            return str.Length;
        }

        public JSONValue decode(string str)
        {
            int index = 0;
            index = passWhiteSpace(str, index);
            if (str[index] == '[')
                this.json = decodeArray(str, ref index);
            if (str[index] == '{')
                this.json = decodeObject(str, ref index);
            return this.json;
        }

    }
}
