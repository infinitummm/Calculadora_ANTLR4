import javax.swing.*;
import java.awt.*;
import java.util.List;

public class PlotWindow extends JPanel {

    private final List<Double> xs;
    private final List<Double> ys;
    private final String title;
    private final Double fixedYmin;
    private final Double fixedYmax;

    public PlotWindow(List<Double> xs, List<Double> ys, String title) {
        this(xs, ys, title, null, null);
    }

    public PlotWindow(List<Double> xs, List<Double> ys, String title, Double fixedYmin, Double fixedYmax) {
        this.xs = xs;
        this.ys = ys;
        this.title = title;
        this.fixedYmin = fixedYmin;
        this.fixedYmax = fixedYmax;

        JFrame frame = new JFrame("Calculadora Grafica - " + title);
        frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        frame.setSize(850, 650);
        frame.setLocationRelativeTo(null);
        frame.add(this);
        frame.setVisible(true);
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2 = (Graphics2D) g;
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);

        int width = getWidth();
        int height = getHeight();
        int margin = 50;

        // Fondo
        g2.setColor(new Color(250, 250, 252));
        g2.fillRect(0, 0, width, height);

        if (xs.size() < 2) {
            g2.setColor(Color.RED);
            g2.drawString("No hay suficientes puntos validos para graficar.", margin, height / 2);
            return;
        }

        // Rango de X
        double xmin = xs.stream().mapToDouble(Double::doubleValue).min().orElse(-1.0);
        double xmax = xs.stream().mapToDouble(Double::doubleValue).max().orElse(1.0);
        if (Math.abs(xmax - xmin) < 1e-9) {
            xmin -= 1.0;
            xmax += 1.0;
        }

        // Rango de Y
        double ymin = (fixedYmin != null) ? fixedYmin : ys.stream().mapToDouble(Double::doubleValue).min().orElse(-1.0);
        double ymax = (fixedYmax != null) ? fixedYmax : ys.stream().mapToDouble(Double::doubleValue).max().orElse(1.0);
        if (Math.abs(ymax - ymin) < 1e-9) {
            ymin -= 1.0;
            ymax += 1.0;
        }

        int plotWidth = width - 2 * margin;
        int plotHeight = height - 2 * margin;

        // Cuadricula
        g2.setColor(new Color(225, 230, 235));
        g2.drawRect(margin, margin, plotWidth, plotHeight);

        // Eje X (y = 0)
        if (ymin <= 0 && ymax >= 0) {
            int pyZero = margin + plotHeight - (int) ((0.0 - ymin) / (ymax - ymin) * plotHeight);
            g2.setColor(new Color(150, 160, 175));
            g2.drawLine(margin, pyZero, margin + plotWidth, pyZero);
            g2.drawString("0", margin - 15, pyZero + 4);
        }

        // Eje Y (x = 0)
        if (xmin <= 0 && xmax >= 0) {
            int pxZero = margin + (int) ((0.0 - xmin) / (xmax - xmin) * plotWidth);
            g2.setColor(new Color(150, 160, 175));
            g2.drawLine(pxZero, margin, pxZero, margin + plotHeight);
            g2.drawString("0", pxZero - 4, margin + plotHeight + 15);
        }

        // Etiquetas de rangos
        g2.setColor(new Color(80, 90, 100));
        g2.setFont(new Font("SansSerif", Font.PLAIN, 11));
        g2.drawString(String.format("x_min: %.2f", xmin), margin, margin + plotHeight + 25);
        g2.drawString(String.format("x_max: %.2f", xmax), margin + plotWidth - 60, margin + plotHeight + 25);
        g2.drawString(String.format("y_max: %.2f", ymax), 5, margin + 12);
        g2.drawString(String.format("y_min: %.2f", ymin), 5, margin + plotHeight);

        // Titulo de la funcion
        g2.setColor(new Color(25, 50, 90));
        g2.setFont(new Font("SansSerif", Font.BOLD, 14));
        g2.drawString("f(x) = " + title, margin, margin - 15);

        // Trazado de la curva
        g2.setColor(new Color(30, 110, 220));
        g2.setStroke(new BasicStroke(2.0f));

        double yRange = ymax - ymin;
        for (int i = 1; i < xs.size(); i++) {
            double x1 = xs.get(i - 1);
            double y1 = ys.get(i - 1);
            double x2 = xs.get(i);
            double y2 = ys.get(i);

            // Filtrar saltos de asintota (discontinuidades como 1/x o tan(x))
            if (Math.abs(y2 - y1) > yRange * 0.75 && (y1 * y2 < 0)) {
                continue;
            }

            int px1 = margin + (int) ((x1 - xmin) / (xmax - xmin) * plotWidth);
            int py1 = margin + plotHeight - (int) ((y1 - ymin) / (ymax - ymin) * plotHeight);

            int px2 = margin + (int) ((x2 - xmin) / (xmax - xmin) * plotWidth);
            int py2 = margin + plotHeight - (int) ((y2 - ymin) / (ymax - ymin) * plotHeight);

            g2.drawLine(px1, py1, px2, py2);
        }
    }
}
