package bi;

import weka.core.Instance;
import weka.core.Instances;
import weka.core.Utils;
import weka.core.converters.ArffLoader;
import weka.core.converters.ArffSaver;

import java.io.*;
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

/**
 * @author solomon
 */
public class RandomGenerator {
    private static String INPUT_FILENAME = "php88ZB4Q.arff";

    private static String OUTPUT_FILENAME = "output.arff";

    private static int SEED = 2;

    private static Map<Integer, Double> MISSING_PERCENTAGES_FOR_COLUMNS = createMissingPercentageForColumns();

    private static Map<Integer, Double> createMissingPercentageForColumns() {
        Map<Integer, Double> missingPercentagesForColumns = new HashMap<>();
        missingPercentagesForColumns.put(188, 0.7); //188 is index -> therefore it is the 189th column as index starts with 0
        missingPercentagesForColumns.put(302, 0.8);
        return missingPercentagesForColumns;
    }


    public static void main(String[] args) {
        double missingValue = Utils.missingValue(); //denotes a missing value in arff
        Random random = new Random(SEED);           //random generator

        try(BufferedReader br = new BufferedReader(new FileReader(INPUT_FILENAME))) {
            ArffLoader.ArffReader arffReader = new ArffLoader.ArffReader(br);
            Instances data = arffReader.getData();

            for(int i = 0; i < data.size(); i++) {
                Instance line = data.get(i);
                MISSING_PERCENTAGES_FOR_COLUMNS.forEach((index, missingPercentage) -> { //loop through map with defined missing values
                    if(random.nextDouble() <= missingPercentage) {
                        line.setValue(index, missingValue);
                    }
                });
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
