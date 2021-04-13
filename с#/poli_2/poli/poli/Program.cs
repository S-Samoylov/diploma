using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace poli
{
    class Program
    {
        //const int LIMIT = 2;
        //public static int LIMIT;

        static void Main(string[] args)
        {
            // init
            int LIMIT;
            string inputVectorString;
            if (args.Length == 2)
            {
                LIMIT = (int)Char.GetNumericValue(args[0][0]);
                inputVectorString = args[1];
            }
            else
            {
                LIMIT = (int)Char.GetNumericValue(Console.ReadLine()[0]);
                //inputVectorString = Console.ReadLine();
                inputVectorString = "1111110110100110";//001101011111110011101101010111101110010001111101";
            }

                int n = (int) Math.Log(inputVectorString.Length, 2);

            int[] inputVector = new int[inputVectorString.Length];

            Conjunction.prepare(LIMIT); //prepare truthvectors for all conj
            Shennon.prepare(LIMIT);

            for (int i = 0; i < inputVectorString.Length; i++)
            {
                inputVector[i] = (int) Char.GetNumericValue(inputVectorString[i]);
            }

            // main part
            List<int> zhigalkin = Zhigalkin.parse(inputVector);

            DateTime start = DateTime.Now;
            List<int> result = Shennon.findParallel(inputVector);
            DateTime end = DateTime.Now;
            /*
            for (int i = 0; i < result.Count(); i++)
            {
                Console.WriteLine(result.ElementAt(i));
            }
            */
            Console.WriteLine(Pol.toCons(result, n));
            //Console.WriteLine("Result: " + Pol.toString(result, n));
            /*
            int[] l = new int[inputVectorString.Length / 2];
            l[0] = 1;
            l[1] = 1;
            l[2] = 1;
            l[3] = 0;
            l[4] = 1;
            l[5] = 1;
            l[6] = 0;
            l[7] = 1;
            List<int> s = Pol.find(l);
            for (int i = 0; i < s.Count; i++)
            {
                Console.Write(" " + s[i]);
            }*/
            //Console.WriteLine("Result length: " + result.Count);
            //Console.WriteLine();
            //Console.WriteLine("Zhigalkin: " + Pol.toString(zhigalkin, n));
            //Console.WriteLine("Zhigalkin length: " + zhigalkin.Count);
            //Console.WriteLine();
            //Console.WriteLine("Time: " + (end - start).TotalSeconds);

            //wait
            //Console.ReadLine();
        }
    }
}
