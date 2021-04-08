using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace poli
{
    class Shennon
    {
        private static int LIMIT;

        private static Dictionary<int[], List<int>> vecValues;

        public static void prepare(int l)
        {
            vecValues = new Dictionary<int[], List<int>>();
            LIMIT = l;
        }

        public static async Task<List<int>> find(int[] vector)
        {
            if (vecValues.ContainsKey(vector))
            {
                return vecValues[vector];
            }

            int n = (int) Math.Log(vector.Length, 2);

            if (n <= LIMIT)
            {
                return Pol.find(vector);
            }

            List<int> minPol = new List<int>();

            for (int i = 0; i < n; i++)
            {
                int j = 0;
                int k = (int) Math.Pow(2, i);

                int l0 = 0;
                int l1 = 0;

                int[] vector0 = new int[vector.Length / 2];
                int[] vector1 = new int[vector.Length / 2];
                int[] vectorSum = new int[vector.Length / 2];

                while (j != vector.Length)
                {
                    if ((j / k) % 2 == 0)
                    {
                        vector0[l0] = vector[j];

                        if (l1 >= l0)
                        {
                            vectorSum[l0] = (vector0[l0] + vector1[l0]) % 2;
                        }

                        l0++;
                    } else
                    {
                        vector1[l1] = vector[j];

                        if (l0 >= l1)
                        {
                            vectorSum[l1] = (vector0[l1] + vector1[l1]) % 2;
                        }

                        l1++;
                    }

                    j++;
                }

                List<int> pol0 = await find(vector0);
                List<int> pol1 = await find(vector1);
                List<int> polSum = await find(vectorSum);

                if (minPol.Count == 0 || pol0.Count + pol1.Count < minPol.Count)
                {
                    minPol = Pol.multiByVar(1, pol1, i);
                    minPol.AddRange(Pol.multiByVar(2, pol0, i));
                }

                if (minPol.Count == 0 || polSum.Count + pol0.Count < minPol.Count)
                {
                    minPol = Pol.multiByVar(1, polSum, i);
                    minPol.AddRange(Pol.multiByVar(0, pol0, i));
                }

                if (minPol.Count == 0 || pol1.Count + polSum.Count < minPol.Count)
                {
                    minPol = Pol.multiByVar(0, pol1, i);
                    minPol.AddRange(Pol.multiByVar(2, polSum, i));
                }
            }

            vecValues[vector] = minPol;

            return minPol;
        }

        public static List<int> findParallel(int[] vector)
        {
            if (vecValues.ContainsKey(vector))
            {
                return vecValues[vector];
            }

            int n = (int)Math.Log(vector.Length, 2);

            if (n <= LIMIT)
            {
                return Pol.find(vector);
            }

            List<int> minPol = new List<int>();
            List<Task<List<int>>> taskPool = new List<Task<List<int>>>();

            for (int i = 0; i < n; i++)
            {
                int j = 0;
                int k = (int)Math.Pow(2, i);

                int l0 = 0;
                int l1 = 0;

                int[] vector0 = new int[vector.Length / 2];
                int[] vector1 = new int[vector.Length / 2];
                int[] vectorSum = new int[vector.Length / 2];

                while (j != vector.Length)
                {
                    if ((j / k) % 2 == 0)
                    {
                        vector0[l0] = vector[j];

                        if (l1 >= l0)
                        {
                            vectorSum[l0] = (vector0[l0] + vector1[l0]) % 2;
                        }

                        l0++;
                    }
                    else
                    {
                        vector1[l1] = vector[j];

                        if (l0 >= l1)
                        {
                            vectorSum[l1] = (vector0[l1] + vector1[l1]) % 2;
                        }

                        l1++;
                    }

                    j++;
                }

                taskPool.Add(find(vector0));
                taskPool.Add(find(vector1));
                taskPool.Add(find(vectorSum));
            }

            for (int i = 0; i < taskPool.Count; i += 3)
            {
                List<int> pol0 = taskPool[i].Result;
                List<int> pol1 = taskPool[i + 1].Result;
                List<int> polSum = taskPool[i + 2].Result;

                if (minPol.Count == 0 || pol0.Count + pol1.Count < minPol.Count)
                {
                    minPol = Pol.multiByVar(1, pol1, i);
                    minPol.AddRange(Pol.multiByVar(2, pol0, i));
                }

                if (minPol.Count == 0 || polSum.Count + pol0.Count < minPol.Count)
                {
                    minPol = Pol.multiByVar(1, polSum, i);
                    minPol.AddRange(Pol.multiByVar(0, pol0, i));
                }

                if (minPol.Count == 0 || pol1.Count + polSum.Count < minPol.Count)
                {
                    minPol = Pol.multiByVar(0, pol1, i);
                    minPol.AddRange(Pol.multiByVar(2, polSum, i));
                }
            }

            vecValues[vector] = minPol;

            return minPol;
        }
    }
}
