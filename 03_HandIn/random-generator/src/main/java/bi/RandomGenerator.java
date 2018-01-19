package bi;

import java.io.*;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

/**
 * @author solomon
 */
public class RandomGenerator
{
    private static String INPUT_FILENAME = "php88ZB4Q.csv";

    private static String OUTPUT_FILENAME = "output.csv";

    private static int SEED = 2;

    private static int SEED_ATTRIBUTE_RANDOMS = 100;

    public static void main(String[] args) {
        try(BufferedReader br = new BufferedReader(new FileReader(INPUT_FILENAME))) {
            StringBuilder outputBuilder = new StringBuilder();
            String line = br.readLine(); //don't replace values on first line
            outputBuilder.append(line).append("\n");
            String[] firstLineAsArray = line.split(",");
            List<Double> missingPercentages = createMissingPercentagesPerAttribute(firstLineAsArray.length -1);
            System.out.println("Missing percentages: " + missingPercentages);
            Random random = new Random(SEED);

            while ((line = br.readLine()) != null) {
                String[] lineAsArray = line.split(",");
                for(int i = 0; i < lineAsArray.length; i++ ) {
                    if(i < missingPercentages.size() && random.nextDouble() <= missingPercentages.get(i)) {
                        lineAsArray[i] = "?";
                    }
                }
                outputBuilder.append(String.join(",", lineAsArray)).append("\n");
            }

            writeToFile(OUTPUT_FILENAME, outputBuilder.toString());
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static void writeToFile(String filename, String outputData) {
        try (Writer writer = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(filename), "utf-8"))) {
            writer.write(outputData);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static List<Double> createMissingPercentagesPerAttribute(int nrAttributes) {
        Random random = new Random(SEED_ATTRIBUTE_RANDOMS);
        List<Double> missingPercentagesPerAttribute = new ArrayList<>();
        for(int i = 0; i < nrAttributes; i++) {
            missingPercentagesPerAttribute.add(random.nextDouble());
        }
        return missingPercentagesPerAttribute;
    }
}
