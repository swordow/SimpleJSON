using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using SharpJSON;
namespace SharpJSON
{
    class Program
    {
        static void Main(string[] args)
        {
            SharpJSON sjson = new SharpJSON("{'val':12.009,'x':'d','a':['a','a','v', 12.31, 0.231, 12321.,'string',{'b': '      dsa', 'c' : [false, true, null, {'a':true}]}],'b':'text','c':{'x':['a',{'x':['d',{'c':['aa',]}]}]}}");
            string x = "";
            sjson.get("b", ref x);
            double v = 0.0;
            sjson.get("val", ref v);
            System.Console.Out.Write(v);
            System.Console.Out.Write(new SharpJSON(sjson.dump()).dump());
        }
    }
}
