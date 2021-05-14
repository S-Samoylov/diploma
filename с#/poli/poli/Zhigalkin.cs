using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace poli
{
    class Zhigalkin
    {
        public static List<int> parse(int[] v)
        {
            int[] vector = new int[v.Length];
            Array.Copy(v, vector, v.Length);

            int n = (int) Math.Log(vector.Length, 2);

            for (int i = 0; i < n; i++)
            {
                int gap = (int) Math.Pow(2, i);
                int j = gap;

                while (j < vector.Length)
                {
                    for (int l = 0; l < gap; l++)
                    {
                        vector[j] = (vector[j] + vector[j - gap]) % 2;
                        j += 1;
                    }

                    j += gap;
                }
            }

            List<int> pol = new List<int>();

            for (int i = 0; i < vector.Length; i++)
            {
                if (vector[i] == 1)
                {
                    if (i == 0)
                    {
                        pol.Add(Conjunction.ONE);
                    } else
                    {
                        int j = i;
                        int tri = 0;
                        int power = 1;
                        
                        while (j > 0)
                        {
                            tri += power * (j % 2);
                            j /= 2;
                            power *= 3;
                        }

                        pol.Add(tri);
                    }
                }
            }

            return pol;
        }
    }
}
