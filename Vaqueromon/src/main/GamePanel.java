package main;

import java.awt.Color;
import java.awt.Graphics;
import javax.swing.JPanel;
import inputs.KeyboardInputs;
import inputs.MouseInputs;

public class GamePanel extends JPanel{

    private MouseInputs mouseInputs;    // Single MouseInputs Object

    public GamePanel() {

        mouseInputs = new MouseInputs(this);        // Instancing MouseInputs
        addKeyListener(new KeyboardInputs(this));
        addMouseListener(mouseInputs);
        addMouseMotionListener(mouseInputs);
    }

    public void paintComponent(Graphics g) {
        super.paintComponent(g);

        g.setColor(new Color(240,240,240));
        g.fillRect(0, 0, 1280, 720);

        g.setColor(Color.RED);
        g.fillRect(540, 350, 200, 200);
        g.setColor(Color.BLACK);
        g.drawString("Your Monster", 540, 570);
        
        g.setColor(Color.BLUE);
        g.fillRect(500, 200, 100, 100);
        g.setColor(Color.BLACK);
        g.drawString("Opponent", 510, 320);
    }
    
}
