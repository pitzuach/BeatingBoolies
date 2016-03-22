import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

/**
 * Created by Matan on 3/22/16.
 */
public class Reader {


    public String readFromTxt(String filename, String parsedString) throws IOException {
        BufferedReader br = null;
        String currentLine;
        br = new BufferedReader(new FileReader("/Users/Matan/IdeaProjects/Anti-Bullying/KS.txt"));
        while ((currentLine = br.readLine()) != null) {
            parsedString.concat(currentLine);
        }
        return parsedString;
    }

}
