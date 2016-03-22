import org.jnativehook.GlobalScreen;
import org.jnativehook.*;
import org.jnativehook.keyboard.NativeKeyListener;
import org.jnativehook.mouse.NativeMouseListener;


/**
 * Created by Matan on 3/22/16.
 */
public class main {
    public static void main(String  args[])  {
        KS k = new KS();
        try{
            //GlobalScreen.removeNativeMouseListener();
            GlobalScreen.registerNativeHook();
            GlobalScreen.addNativeKeyListener(k);
            //GlobalScreen.removeNativeMouseListener(NajkjjjtiveMouseListener.class);
        }

        catch (Exception ex) {
            System.err.println("There was a problem registering the native hook.");
            System.err.println(ex.getMessage());

            System.exit(1);
        }

    }




    }

