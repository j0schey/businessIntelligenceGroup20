package at.ac.tuwien.bi.g20;

import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

/**
 * Sentiment analysis on Amazon product reviews.
 *
 * VU Business Intelligence WS 2017 - Group 20
 *
 * built with code excerpts from:
 * https://www.cloudera.com/documentation/other/tutorial/CDH5/topics/ht_example_4_sentiment_analysis.html
 */
public class SentimentAmazon extends Configured implements Tool{

    public static void main( String[] args ) throws Exception {
        int res = ToolRunner.run(new SentimentAmazon(), args);
        System.exit(res);
    }

    public int run(String[] args) throws Exception {
        Job job = Job.getInstance(getConf(), "sentimentAmazon");
        for (int i = 0; i < args.length; i += 1) {
            if ("-pos".equals(args[i])) {
                job.getConfiguration().setBoolean("sentimentAmazon.pos.patterns", true);
                i += 1;
                job.addCacheFile(new Path(args[i]).toUri());
            }
            if ("-neg".equals(args[i])) {
                job.getConfiguration().setBoolean("sentimentAmazon.neg.patterns", true);
                i += 1;
                job.addCacheFile(new Path(args[i]).toUri());
            }
        }

        // standard job methods
        Path outputDir = new Path(args[1]);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, outputDir);

        job.setMapperClass(Map.class);
        job.setReducerClass(Reduce.class);

        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(Text.class);

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(DoubleWritable.class);

        // delete output directory if it exists
        FileSystem hdfs = FileSystem.get(job.getConfiguration());
        if (hdfs.exists(outputDir)) {
            hdfs.delete(outputDir, true);
        }

        int result = job.waitForCompletion(true) ? 0 : 1;

        return result;
    }
}
