using System;
using System.IO;
using System.Collections.Generic;
using System.Reflection;

using MapShots.COM.FODM;
using MapShots.Utilities.COM;
using MapShots.FODDs.fodPrecisionPlanting;


namespace PPFoddDemo
{
    class Program
    {
        static IfoFactory factory = mpnObjectManager.CreateObject("FODM.foFactory") as IfoFactory;

        static void Main(string[] args)
        {
            IfoFODD ppFodd = new fodPrecisionPlantingReader();
            Console.Write(ppFodd.Name);

            string path = @"C:\CardData\PP2020\Raw\";
            DirectoryInfo dir = new DirectoryInfo(path);
            FileInfo[] datFiles = dir.GetFiles("field_map*.dat");

            IfoFiles fileList = mpnObjectManager.CreateObject("FODM.foFiles") as IfoFiles;
            foreach (FileInfo file in datFiles)
            {
                IfoFile foFile = getFoFile(file);
                if (foFile != null)
                {
                    fileList.Add(foFile);
                }
            }

            IfoSummary summary = mpnObjectManager.CreateObject("FODM.foSummary") as IfoSummary;
            IfoSummaryLoader loader = factory.GetSummaryLoader(summary);

            bool result = ppFodd.ReadFiles(loader, fileList, null);

            Console.WriteLine(result);
        }

        private static IfoFile getFoFile(FileInfo file)
        {
            Type t = typeof(fodPrecisionPlantingPlantingFile);

            Type[] conTypes = new Type[] { typeof(string), typeof(string) };
            ConstructorInfo fileConstructor = t.GetConstructor(BindingFlags.NonPublic | BindingFlags.Instance, null, conTypes, null);

            object[] param = new object[] { file.FullName, "" };
            IfoFile foFile = fileConstructor.Invoke(param) as IfoFile;
            return foFile;
        }

    }
}