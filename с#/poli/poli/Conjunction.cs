using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace poli
{
    class Conjunction
    {
        public static int ONE;

        public static int[] conValues;

        public static void prepare(int n)
        {
            int argMax = (int)Math.Pow(2, n);
            int length = (int) Math.Pow(3, n);
            ONE = length;

            //prepare for all con
            conValues = new int[length + 1];

            for (int i = 0; i < length; i++)
            {
                int thruthVector = 0;
                int power = 1;

                for (int j = 0; j < argMax; j++)
                {
                    thruthVector += power * value(i, j);
                    power *= 2;
                    //if (i == 1) Console.WriteLine("thruthVector" + i.ToString() + "=" + thruthVector.ToString());
                }
                if (true)
                {
                    
                   //Console.WriteLine("thruthVector " + i.ToString() + " "+ Conjunction.toString(i,n) + " " + thruthVector.ToString());
                }
                conValues[i] = thruthVector;
            }

            conValues[ONE] = (int) Math.Pow(2, argMax) - 1;

        }

        public static string toString(int con, int n)
        {
            if (con == ONE)
            {
                return "1";
            }

            int index = 0;
            string result = "";

            while (con > 0)
            {
                int triDigit = con % 3;
                con /= 3;

                if (triDigit > 0)
                {
                    if (triDigit == 2)
                    {
                        result += "~";
                    }

                    result += "x" + (n - index);
                }

                index++;
            }

            return result;
        }

        public static string toCons(int con, int n)
        {
            if (con == ONE)
            {
                return "3";
            }

            int index = 0;
            string result = "";

            while (con > 0)
            {
                int triDigit = con % 3;
                con /= 3;

                if (triDigit == 0) result += "0";
                if (triDigit == 1) result += "1";
                if (triDigit == 2) result += "2";

                index++;
            }

            return result;
        }

        private static int value(int con, int arg)
        {
            if (con == 0)
            {
                return 0;
            }

            int value = 1;

            while (con > 0)
            {
                int binDigit = arg % 2;
                int triDigit = con % 3;

                if (triDigit == 1)
                {
                    value *= binDigit;
                }

                if (triDigit == 2)
                {
                    value *= (binDigit + 1) % 2;
                }

                arg /= 2;
                con /= 3;
            }
            return value;
        }
    }
}
