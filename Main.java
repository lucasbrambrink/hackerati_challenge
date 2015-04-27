import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.io.*;

public class Main {
	
	private static Boolean numbersAreConsecutive(int[] slice){
		boolean isAscending = slice[0] + 1 == slice[1];
		for (int i = 0; i + 1 < slice.length; i++){
			int item = slice[i];
			int next = slice[i + 1];
			int nextInSequence = isAscending ? item + 1 : item - 1;
			if (nextInSequence != next){
				return false;
			}
		}
		return true;
	}
	
	private static List<Integer> findConsecutiveRuns(int[] array){
		List<Integer> indexesOfRuns = new ArrayList<Integer>();
		for (int index = 0; index + 3 < array.length; index++){
			int[] sliceOfThree = Arrays.copyOfRange(array, index, index + 3);
			boolean isRunIndex = Main.numbersAreConsecutive(sliceOfThree);
			if (isRunIndex){
				indexesOfRuns.add(index);
			}
		}
		return indexesOfRuns;
	}

	public static void main(String[] args) {
		int[] example1 = {1, 2, 3, 5, 10, 9, 8, 9, 10, 11, 7};
		System.out.println(findConsecutiveRuns(example1));
	}

}
