/**
 * Created by Matan on 3/22/16.
 */

import java.awt.*;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

public class Writer {
    public static void WriteToFile(String content) {
        try {

BufferedWriter bw=null;

            File file = new File("/Users/Matan/IdeaProjects/Anti-Bullying/KS.txt");

            // if file does not exists, then create it
            if (!file.exists()) {
                file.createNewFile();
            }

            bw = new BufferedWriter(new FileWriter(file, true));
            if (content.equals("Space")) {
                bw.write(" ");
            } else if (content.equals("Backspace")) {
                bw.write("~");
            } else if (content.equals("Slash")) {
                bw.write("/");
            } else if (content.equals("Period")) {
                bw.write(".");
            } else if (content.equals("Comma")) {
                bw.write(",");
            } else {
                bw.write(content);
            }

            bw.flush();
            bw.close();

           /* FileWriter fw = new FileWriter(file.getAbsoluteFile());
            BufferedWriter bw = new BufferedWriter(fw);
            bw.append(content);
            bw.close();*/

            System.out.println("Done");

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}


/*

 */