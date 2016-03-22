import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;

/**
 * Created by Matan on 3/22/16.
 */
public class Reader {


    public ReadType readFromTxt(String filename, String parsedString) throws IOException {
        BufferedReader br = null;
        String currentLine;
        br = new BufferedReader(new FileReader("/Users/Matan/IdeaProjects/Anti-Bullying/KS.txt"));
        while ((currentLine = br.readLine()) != null) {
            parsedString.concat(currentLine);
        }
        ReadType readType = new ReadType((int) (long) br.lines().count(), parsedString);
        return readType;
    }
}
