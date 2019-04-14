import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.Optional;
import java.util.Scanner;

public class Main {

	public static void main(String[] args) {
		if(args.length > 2) {
			File file = new File(args[0]);
			if(!file.exists()) {
				System.out.println("Ficheiro nao existe");
			}
			try {
				Scanner sc = new Scanner(new FileReader(file));
				String line;
				String[] lines;
				sc.nextLine();
				sc.nextLine();
				sc.nextLine();
				
				line= sc.nextLine();
				int numDomains = Integer.valueOf(line);
				ArrayList<Domain> domains = new ArrayList<Domain>();
				for(int i = 0; i<numDomains;i++) {
					Domain t = new Domain();
					line = sc.nextLine();
					lines = line.split(" ");
					t.name = lines[0];
					lines = lines[1].split("..");
					t.a = Integer.valueOf(lines[0]);
					t.b = Integer.valueOf(lines[1]);
					domains.add(t);
				}
				sc.nextLine();
				sc.nextLine();
				line = sc.nextLine();
				int numVariaveis = Integer.valueOf(line);
				ArrayList<Variaveis> variaveis = new ArrayList<Variaveis>();
				for(int i = 0; i<numVariaveis;i++) {
					line = sc.nextLine();
					lines = line.split(" ");
					Variaveis var = new Variaveis();
					var.name = lines[0];
					for(int k =1; k< lines.length ;k++) {
						final String abc = lines[k];
						Optional<Domain> dd =domains.stream().filter((Domain d) -> abc.equals(d.name)).findFirst();
						if(dd.isPresent()) {
							var.domains.add(dd.get());
						}
					}
					variaveis.add(var);
					
				}
				sc.nextLine();
				sc.nextLine();
				line = sc.nextLine();
				int numConstraints = Integer.valueOf(line);
				ArrayList<Constraint> cons = new ArrayList<Constraint>();
				sc.nextLine();
				for(int i = 0; i<numConstraints;i++) {
					Constraint constraint = new Constraint();
					sc.nextLine();
					sc.nextLine();
					constraint.numVar = Integer.valueOf(sc.nextLine());
					for(int j = 0; j<constraint.numVar;j++) {
						constraint.var.add(sc.nextLine());
					}
					constraint.decisao = sc.nextLine();
					constraint.numDecisao = Integer.valueOf(sc.nextLine());
					for(int j = 0; j<constraint.numDecisao;j++) {
						lines = sc.nextLine().split(" ");
						constraint.paresDec.add(new ArrayList<Integer>());
						for(int k=0;k<constraint.numVar;k++) {
							constraint.paresDec.get(i).add(Integer.valueOf(lines[k]));
						}
					}
					sc.nextLine();
					cons.add(constraint);
				}
				
				
			} catch (FileNotFoundException e) {
				e.printStackTrace();
			}
			
		}else {
			System.out.println("Tem de passar um ficheiro csp e posteriormente o nome do ficheiro de destino");
		}
	}

}
