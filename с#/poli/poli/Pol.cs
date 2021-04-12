using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace poli
{
    class Pol
    {
        private static int inputValue;

        private static int threshold;

        public static List<int> find(int[] vector)
        {
            inputValue = 0;
            int power = 1;

            for (int i = 0; i < vector.Length; i++)
            {
                inputValue += vector[i] * power;
                power *= 2;
            }
            //Console.WriteLine("ttt" + inputValue.ToString());
            List<int> zhigalkin = Zhigalkin.parse(vector);
            threshold = zhigalkin.Count;
            //Console.WriteLine("zh" + threshold.ToString());
            List<int> result = walkTree(0, 0, 0);
            //Console.WriteLine("res " + result[0].ToString());
            if (result.Count == 0)
            {
                result = zhigalkin;
            }
            else
            {
                result.RemoveAt(result.Count - 1);
            }

            return result;
        }

        public static List<int> multiByVar(int var, List<int> pol, int place, bool afterWalkTree = false)
        {
            List<int> result = new List<int>();

            for (int i = 0; i < pol.Count; i++)
            {
                int con = pol[i];
                int newCon = con;
                int power = 1;

                for (int j = 0; j < place; j++)
                {
                    newCon /= 3;
                    power *= 3;
                }
                if (afterWalkTree)
                {
                    if (con != Conjunction.ONE)
                    {
                        newCon = (newCon * 3 + var) * power + (con % power);
                    }
                    else
                    {
                        if (var > 0)
                        {
                            newCon = var * power;
                        }
                        else
                        {
                            newCon = con;
                        }
                    }
                }
                else
                {
                    newCon = (newCon * 3 + var) * power + (con % power);
                }
                result.Add(newCon);
            }

            return result;
        }

        public static string toString(List<int> pol, int n)
        {
            string result = "";

            for (int i = 0; i < pol.Count; i++)
            {
               result += Conjunction.toString(pol[i], n);

                if (i != pol.Count - 1)
                {
                    result += " + ";
                }
            }

            return result;
        }

        public static string toCons(List<int> pol, int n)
        {
            string result = "";

            for (int i = 0; i < pol.Count; i++)
            {
                result += Conjunction.toCons(pol[i], n);

                if (i != pol.Count - 1)
                {
                    result += ",";
                }
            }

            return result;
        }

        private static List<int> walkTree(int currentConNumber, int currentPolValue, int depth)
        {
            if (currentPolValue == inputValue)
            {
                List<int> l =  new List<int>() { currentConNumber };
                //Console.WriteLine("count " + l.Count.ToString() + " currentnum " + l[0].ToString());
                return l;
            }

            if (depth == threshold)
            {
                return new List<int>();
            }

            List<int> minPol = new List<int>();
            for (int i = currentConNumber + 1; i < Conjunction.conValues.Length; i++)
            {
                int vecSum = Conjunction.conValues[i] ^ currentPolValue;
                //if (i == 1) Console.WriteLine(i.ToString() + " vecSum " + vecSum.ToString()); 
                List<int> result = walkTree(i, vecSum, depth + 1);

                if (result.Count > 0 && (minPol.Count == 0 || result.Count + 1 < minPol.Count))
                {
                    minPol = result;
                    minPol.Add(currentConNumber);
                }
            }
            /*
            if (minPol.Count > 0)
            {
                Console.WriteLine("Start");
                for (int i = 0; i < minPol.Count; i++)
                {
                    Console.Write(minPol[i].ToString() + ' ');
                }
                Console.WriteLine();
            }*/
            return minPol;
        }
    }
}
