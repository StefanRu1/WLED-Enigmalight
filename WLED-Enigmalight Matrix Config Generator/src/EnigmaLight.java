import java.io.FileWriter;   // Import the FileWriter class
import java.io.IOException;  // Import the IOException class to handle errors
import java.text.DecimalFormat;
import java.text.NumberFormat;
import java.util.Locale;

public class EnigmaLight {	

	  public static void main(String[] args) {
	    try {
	    	
	    //args 0 = ip, 1 = port, 2 = name, 3 = x, 4 = y, 5 = invert
	    // Wrong number of arguments
	    if ( args.length != 6 )
	    {
	    System.out.println( "EnigmaLight Matrix Config Writer" );
	    System.out.println( "v0.5 by stefanru" );
	    System.out.println( "-------------------------" );
	    System.out.println( "You have to pass 6 arguments" );
	    System.out.println( "EnigmaLight <IP> <PORT> <DEVICENAME> <NR OF LIGHTS ON X-AXIS> <NR OF LIGHTS ON Y-AXIS> <INVERT EVERY 2ND LINE>" );
	    System.out.println( "WLED standard UDP port is: 21324, INVERT EVERY 2ND LINE is 0 or 1" );
	    System.out.println( "e.g. EnigmaLight 192.168.69.5 21324 TestLight 10 11 0" );
	    System.out.println( " " );
	    System.out.println( "More Infos about EnigmaLight can be found here:" );
	    System.out.println( "https://board.newnigma2.to/wbb4/index.php/Thread/32156-EnigmaLight-pclin-edition/" );
	    return;
	    }
	    
	    // Arguments correct. Begin using them
	    System.out.println( "EnigmaLight Matrix Config Writer" );
	    System.out.println( "v0.1 by stefanru" );
	    System.out.println( "-------------------------" );
	    System.out.println( "Set IP to " + args[0] );
	    System.out.println( "Set PORT to " + args[1] );
	    System.out.println( "Set DEVICENAME to " + args[2] );
	    System.out.println( "Set NR OF LIGHTS ON X-AXIS to " + args[3] );
	    System.out.println( "Set NR OF LIGHTS ON Y-AXIS to " + args[4] );
	    System.out.println( "Set INVERT EVERY 2ND LINE to " + args[5] );
	    String ip = args[0];  		             // IP of WLED Device
	    String port = args[1];				     // UDP Port of WLED Device
	    String lightname = args[2];	             // Devicename
	    double x = Double.parseDouble(args[3]);	 // LEDs on X axis    
	    double y = Double.parseDouble(args[4]);	 // LEDs on Y axis
	    boolean invertlines = false;             // Invert every 2nd line
	    if (args[5] == "1")
	    {
	      invertlines = true;          
	    }
	    System.out.println( "" );
	    System.out.println( "Calculating File ..." );
	      String output = "python /usr/wled_DRGB_numpy.py " + ip +" " + port ;
	      int lightnum = 0;	      
	      int channels = (int) (x*y*3);
	      int channel = 0;
	      double h1;
	      double h2;
	      double v1;
	      double v2;
	      NumberFormat nf = NumberFormat.getNumberInstance(Locale.ENGLISH);
	      DecimalFormat df = new DecimalFormat("#.##");
	      df = (DecimalFormat)nf;
	      
	      
	      
	      FileWriter myWriter = new FileWriter("enigmalight_matrix.conf");
	      
	      // Write EnigmaLight Header
	      myWriter.write("[global]\n");
	      myWriter.write("interface localhost\n");
	      myWriter.write("port 19333"+"\n");
	      myWriter.write("\n");
	      myWriter.write("[color]\n");
	      myWriter.write("name red\n");
	 	  myWriter.write("rgb FF0000\n");
	      myWriter.write("gamma 1.00\n");
	      myWriter.write("adjust 0.90\n");
	      myWriter.write("blacklevel 0.0\n");
	      myWriter.write("\n");
	      myWriter.write("[color]\n");
	      myWriter.write("name green\n");
	      myWriter.write("rgb 00FF00\n");
	      myWriter.write("gamma 1.00\n");
	      myWriter.write(" adjust 1.0\n");
	      myWriter.write("blacklevel 0.0\n");
	      myWriter.write("\n");
	      myWriter.write("[color]\n");
	      myWriter.write("name blue\n");
	      myWriter.write("rgb 0000FF\n");
	      myWriter.write("gamma 1.00\n");
	      myWriter.write("adjust 1.0\n");
	      myWriter.write("blacklevel 0.0\n");
	      myWriter.write("\n");
	      
	      myWriter.write("[device]\n");
	      myWriter.write("name            "+lightname+"\n");
	      myWriter.write("output          "+output+"\n");
	      myWriter.write("channels        "+channels+"\n");
	      myWriter.write("type            popen\n");
	      myWriter.write("interval        40000\n");
	      myWriter.write("debug           off\n");
	      myWriter.write("\n");
	      
	      for (int j = (int)y; j > 0; j--) {	    	  
	      for (int i = 1; i < x+1; i++) {    	 
	    	  
	    	  lightnum++; 
	    	  myWriter.write("[light]\n");
	    	  myWriter.write("position      top\n");
	    	  myWriter.write("name          "+String.format("%03d", lightnum)+"\n");
	    	  channel++;
	    	  myWriter.write("color         red     "+lightname+" "+channel+"\n");
	    	  channel++;
	    	  myWriter.write("color         green   "+lightname+" "+channel+"\n");
	    	  channel++;
	    	  myWriter.write("color         blue    "+lightname+" "+channel+"\n");
	    	  
	    	  if (invertlines && j %2 == 0) {
	    		  h1=100/x*(x-i);    
		    	  h2=100/x*(x-(i-1));
	    	  } else {
	    	  h1=100/x*(i-1);	  
	    	  h2=100/x*i;
	    	  }
	    	  v1=100/y*(j-1);
	    	  v2=100/y*j;
	    	  myWriter.write("hscan         "+df.format(h1)+" "+df.format(h2)+"\n");
	    	  myWriter.write("vscan         "+df.format(v1)+" "+df.format(v2)+"\n");
	    	  myWriter.write("\n");
			
		  }
	     }	    		  
	      
	      myWriter.close();
	      System.out.println( " " );
	      System.out.println("Successfully wrote to the file enigmalight_matrix.conf.");
	      System.out.println( " " );
		  System.out.println( "More Infos about EnigmaLight can be found here:" );
		  System.out.println( "https://board.newnigma2.to/wbb4/index.php/Thread/32156-EnigmaLight-pclin-edition/" );
	    } catch (IOException e) {
	      System.out.println("An error occurred.");
	      System.out.println( "Stacktrace: " );
	      e.printStackTrace();
	      System.out.println( " " );
		  System.out.println( "More Infos about EnigmaLight can be found here:" );
		  System.out.println( "https://board.newnigma2.to/wbb4/index.php/Thread/32156-EnigmaLight-pclin-edition/" );
	     
	    }
	  }
	}
	


