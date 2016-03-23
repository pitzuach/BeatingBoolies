import org.jnativehook.GlobalScreen;
import org.jnativehook.*;
import org.jnativehook.keyboard.NativeKeyListener;
import org.jnativehook.mouse.NativeMouseListener;

import java.util.concurrent.ConcurrentLinkedQueue;


/**
 * Created by Matan on 3/22/16.d
 */
public class main {
    public static void main(String  args[])  {
        KS kk = new KS();

        String Tocheck = "asdvasgd s hdvasjhd shdvahsdvhasvdjas d ajshdajhsvdjhasd sajhd hjas d";
        int iterator = 0;
        while (iterator < Tocheck.length()) {
            kk.handleKey(String.valueOf(Tocheck.charAt(iterator)));
            iterator++;

        }
        ConcurrentLinkedQueue<String> s = kk.sniffs;


        try{
            //GlobalScreen.removeNativeMouseListener();

            GlobalScreen.registerNativeHook();
            GlobalScreen.addNativeKeyListener(kk);
            //GlobalScreen.removeNativeMouseListener(NajkjjjtiveMouseListener.class);
        }

        catch (Exception ex) {
            System.err.println("There was a problem registering the native hook.");
            System.err.println(ex.getMessage());

            System.exit(1);
        }

    }




    }

