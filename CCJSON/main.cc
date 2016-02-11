/*
** created by swordow on 01/26/2016
*/

#include "ccjson.h"

int main()
{
	JSON json("{'val':12.009,'x':'d','a':['a',{'a':'v'}, 12.31, 0.231, 12321.,'string',{'b': '      dsa', 'c' : [false, true, null, {'a':true}]}],'b':'text','c':{'x':['a',{'x':['d',{'c':['aa',]}]}]}}");
	char str[1024] = { 0 };
	printf("%s\n", json.dump(str));
	json.getString("x", str, 0);
	printf("%s\n", str);
}
