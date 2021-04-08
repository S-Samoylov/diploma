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
                inputVectorString = Console.ReadLine();
                //inputVectorString = "1001000010110001101000010101101010000001010111011010110001100011010110011000101010000110001100111010111010101100011000011011000110000011101111001100010100010001000110010011111101101010011111111100100101111101110100100101100010100011101110010010101001100001";
            }

            int n = (int) Math.Log(inputVectorString.Length, 2);

            int[] inputVector = new int[inputVectorString.Length];

            Conjunction.prepare(LIMIT);
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
            Console.WriteLine(Pol.toCons(result, n));
            //Console.WriteLine("Result: " + Pol.toString(result, n));
            //Console.WriteLine("Result length: " + result.Count);
            //Console.WriteLine();
            //Console.WriteLine("Zhigalkin: " + Pol.toString(zhigalkin, n));
            //Console.WriteLine("Zhigalkin length: " + zhigalkin.Count);
            //Console.WriteLine();
            //Console.WriteLine("Time: " + (end - start).TotalSeconds);

            // wait
            //Console.ReadLine();
        }
    }
}
