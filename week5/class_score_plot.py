import matplotlib.pyplot as plt

def read_data(filename):
    data = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            if not line.startswith('#'): # If 'line' is not a header
                data.append([int(word) for word in line.split(',')])
    return data

if __name__ == '__main__':
    # Load score data
    class_kr = read_data('data/class_score_kr.csv')
    class_en = read_data('data/class_score_en.csv')

    # TODO) Prepare midterm, final, and total scores
    midterm_kr, final_kr = zip(*class_kr)
    total_kr = [40/125*midterm + 60/100*final for (midterm, final) in class_kr]
    midterm_en, final_en = zip(*class_en)
    total_en = [40/125*midterm + 60/100*final for (midterm, final) in class_en]

    # TODO) Plot midterm/final scores as points
    plt.subplot(2, 1, 1)
    plt.scatter(midterm_kr, final_kr, label='Korean', color='red', marker='o', s=30, alpha=0.7)
    plt.scatter(midterm_en, final_en, label='English', color='blue', marker='+', s=50, alpha=0.7)
    plt.xlabel('Midterm scores')
    plt.ylabel('Final scores')
    plt.xlim([0, 125])
    
    plt.ylim([0, 100])
    plt.grid(True)
    plt.legend()
    
    # TODO) Plot total scores as a histogram
    plt.subplot(2, 1, 2)
    plt.hist(total_kr, bins=20, range=(0, 100), alpha=0.9, label='Korean', color='red')
    plt.hist(total_en, bins=20, range=(0, 100), alpha=0.2, label='English', color='blue')
    plt.xlabel('Total scores')
    plt.ylabel('The number of students')
    plt.xlim([0, 100])
    plt.legend(loc='upper left')

    plt.tight_layout()
    plt.show()