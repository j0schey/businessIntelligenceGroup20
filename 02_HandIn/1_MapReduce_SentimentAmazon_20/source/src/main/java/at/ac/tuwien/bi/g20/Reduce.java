package at.ac.tuwien.bi.g20;

import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.util.StringUtils;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.net.URI;
import java.util.HashSet;
import java.util.Set;
import java.util.regex.Pattern;

public class Reduce extends Reducer<Text, Text, Text, DoubleWritable> {

    // sets for the positive and negative words
    private static Set<String> posWords = new HashSet<String>();
    private static Set<String> negWords = new HashSet<String>();

    // word boundary defined as whitespace-characters-word boundary-whitespace
    private static final Pattern WORD_BOUNDARY = Pattern.compile("\\s*\\b\\s*");

    @Override
    protected void reduce(Text key, Iterable<Text> values, Reducer<Text, Text, Text, DoubleWritable>.Context context)
            throws IOException, InterruptedException {
        double countPositive = 0, countNegative = 0;

        // iterate over each word in each review text for given product id
        for(Text reviewText : values){
            for(String word : WORD_BOUNDARY.split(reviewText.toString())){

                if(word.isEmpty()){
                    continue;
                }

                // check if current word is positive or negative
                if(posWords.contains(word.toLowerCase())){
                    countPositive++;
                } else if(negWords.contains(word.toLowerCase())){
                    countNegative++;
                }
            }
        }

        // calculate sentiment score
        double sentimentScore = (countPositive - countNegative) / (countPositive + countNegative);

        // set product id and according sentiment score as output
        context.write(key, new DoubleWritable(sentimentScore));
    }

    @Override
    protected void setup(Context context) throws IOException, InterruptedException {
        URI[] localPaths = context.getCacheFiles();

        int uriCount = 0;

        parsePositive(localPaths[uriCount++]);
        parseNegative(localPaths[uriCount]);
    }

    private void parseNegative(URI negWordsUri) {
        try {
            BufferedReader fis = new BufferedReader(new FileReader(
                    new File(negWordsUri.getPath()).getName()));
            String badWord;
            while ((badWord = fis.readLine()) != null) {
                negWords.add(badWord);
            }
        } catch (IOException ioe) {
            System.err.println("Caught exception while parsing cached file '"
                    + negWords + "' : " + StringUtils.stringifyException(ioe));
        }
    }

    private void parsePositive(URI posWordsUri) {
        try {
            BufferedReader fis = new BufferedReader(new FileReader(
                    new File(posWordsUri.getPath()).getName()));
            String goodWord;
            while ((goodWord = fis.readLine()) != null) {
                posWords.add(goodWord);
            }
        } catch (IOException ioe) {
            System.err.println("Caught exception parsing cached file '"
                    + posWords + "' : " + StringUtils.stringifyException(ioe));
        }
    }
}