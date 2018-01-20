package bi;

import weka.core.Instance;
import weka.core.Instances;
import weka.core.Utils;
import weka.core.converters.ArffLoader;
import weka.core.converters.ArffSaver;
import weka.core.converters.CSVLoader;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.Random;

/**
 * @author solomon
 */
public class RandomGenerator
{
    private static String INPUT_FILENAME = "php88ZB4Q.arff";

    private static String OUTPUT_FILENAME = "output(LargeMVOnAllDataSet).arff";

    private static int SEED = 2;

    private static double OVERALL_PERCENTAGE_MISSING = 0.9;


    public static void main(String[] args) {
        double missingValue = Utils.missingValue(); //denotes a missing value in arff
        Random random = new Random(SEED);           //random generator

        try(BufferedReader br = new BufferedReader(new FileReader(INPUT_FILENAME))) {
            ArffLoader.ArffReader arffReader = new ArffLoader.ArffReader(br);
            Instances data = arffReader.getData();

            for(int i = 0; i < data.size(); i++) {
                Instance line = data.get(i);
                for(int j=0; j<line.numAttributes(); j++) {
                    if(random.nextDouble() <= OVERALL_PERCENTAGE_MISSING) {
                        line.setValue(j, missingValue);
                    }
                }
            }

            writeToFile(OUTPUT_FILENAME, data);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static void writeToFile(String filename, Instances outputData) {
        try {
            ArffSaver saver = new ArffSaver();
            saver.setInstances(outputData);
            saver.setFile(new File(filename));
            saver.writeBatch();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
