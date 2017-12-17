package at.ac.tuwien.bi.g20;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;

public class Map extends Mapper<LongWritable, Text, Text, Text> {

    // helper fields to store the product id and the review text
    private Text productId = new Text();
    private Text reviewText = new Text();

    // object mapper to parse the reviews from JSON to Java objects
    private ObjectMapper objectMapper = new ObjectMapper();

    // identifiers of the respective JSON fields
    private static final String JSON_FIELD_PRODUCT_ID = "asin";
    private static final String JSON_FIELD_REVIEW_TEXT = "reviewText";

    @Override
    protected void map(LongWritable key, Text value, Mapper<LongWritable, Text, Text, Text>.Context context)
            throws IOException, InterruptedException {
        String line = value.toString();

        // get product id and review text
        JsonNode jsonObject = objectMapper.readTree(line);
        productId.set(jsonObject.get(JSON_FIELD_PRODUCT_ID).textValue());
        reviewText.set(jsonObject.get(JSON_FIELD_REVIEW_TEXT).textValue());

        // set product id and review text as output
        context.write(productId, reviewText);
    }
}
