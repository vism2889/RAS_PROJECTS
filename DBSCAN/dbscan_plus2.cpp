// AUTHOR: Morgan Visnesky
// DATE: 07/18/20
// FILENAME: dbscan_plus.cpp
//
// DESCRIPTION:
// Beginnings of a C++ implementation of DBSCAN algorithm.
//
# include <iostream>
# include <vector>
# include <math.h>
using namespace std;


class Point
{
public:
  int x;
  int y;
  int z;
  int label;
  std::vector<Point> neighbors;
};

float distFunc(Point a, Point b);
std::vector<Point> regionQuery(std::vector<Point> database, int p, float epsilon);
void growCluster(std::vector<Point> database, std::vector<int> labels, int p, int c, float epsilon, int MinPts);
std::vector<int> myDbscan(std::vector<Point> database, float epsilon, int minPts);

int main()
{
  std::vector<Point> database;
  for (int i = 0; i < 20; i++)
  {
    Point p;
    p.x = i*i;
    p.y = i*i;
    p.z = i*i;
    database.push_back(p);
    //cout << database[i].x;
  }
  cout << endl;
  for (int i = 0; i < 5;i++)
  {
    //cout << endl;
    //cout << "Hey";
    //cout << endl;
    cout << database[i].x << database[i].y << database[i].z;
    cout << endl;
  }

  cout << "distance function: ";
  cout << "hey " << distFunc(database[2], database[3]);
  cout << endl;


  std::vector<int> clusterLabelList = myDbscan(database,40,4);
  //cout << clusterLabelList.size() << "size";

  for (int i = 0; i < clusterLabelList.size(); i++)
  {
    cout << clusterLabelList[i] << " ";
  }


  return 0;
}




float distFunc(Point a, Point b)
{
  float dist = sqrt(pow(b.x-a.x, 2) + pow(b.y-a.y, 2) + pow(b.z-a.z, 2));
  //cout << dist << endl;
  return dist;
}

std::vector<Point> regionQuery(std::vector<Point> database, int p, float epsilon)
{
  cout <<"      "<< "inside regionQuery" << endl;
  std::vector<Point> neighbors;
  for (int i = 0; i < database.size(); i++)
  {
    if (distFunc(database[p],database[i]) < epsilon)
    {
      neighbors.push_back(database[i]);
    }
  }
  return neighbors;
}

void growCluster(std::vector<Point> database, std::vector<int> labels, int p, int c, float epsilon, int minPts)
{
  cout << "inside grow cluster" << endl;
  std::vector<int> searchQueue (0);
  searchQueue.push_back(p);
  cout <<"search ques"<< searchQueue[0]<< endl;
  int i = 0;
  while (i < searchQueue.size())
  {
    p = searchQueue[i];
    cout <<"    "<<"search queueLoop "<< searchQueue[i]<< endl;
    std::vector<Point> neighborPts = regionQuery(database, p, epsilon);
    //std::vector<Point>::iterator it;
    cout <<"        "<< "size neightbors " << neighborPts.size()<< " label i "<< labels[i] <<endl;
    if (neighborPts.size() < minPts)
    {
      cout << "less than min pts"<< endl;
      i = i + 1;
      continue;
    }
    for (Point& j : neighborPts) //(int j = 0; j < neighborPts.size(); j++)
    {
      std::vector<Point>::iterator it = std::find(labels.begin(), labels.end(),j);
      //cout << it;
      if (it != labels.end())
      {
        p = distance(labels.begin(), it);
        if (labels[p] == -1)
        {
          labels[p] = c;
        }
        else if (labels[p] == 0)
        {
          labels[p] = c;
          //cout <<"          "<< labels[it] << " labels j: " << endl;
          searchQueue.push_back(c);
        }
        //cout << labels[it] <<"         "<< "labels j:" <<endl;
      }

    }
    i = i + 1;
  }
}

std::vector<int> myDbscan(std::vector<Point> database, float epsilon, int minPts)
{
  cout <<"size"<< database.size() << endl;
  int d = database.size();
  std::vector<int> labels;
  for (int i = 0; i < d; i++)
  {
    //cout << labels[0];
    labels.push_back(0);

  }
  for (int i = 0; i < labels.size(); i++)
  {
    cout << "labels inside dbscan " <<labels[i] << endl;
  }


  int c = 0;



  for (int i = 0; i < database.size(); i++)
  {
    if (labels[i] != 0)
    {
      cout << "label is zero : "<< endl;
      continue;
    }
    std::vector<Point> neighborPts = regionQuery(database, i, epsilon);
    cout <<"size: "<< neighborPts.size() << endl;
    if (neighborPts.size() < minPts)
    {
      cout << "less than"<< endl;
      labels.at(i) = -1;
      cout << "label at i: " << labels[i]<< endl;
    }
    else
    {
      cout << "default ";
      c = c + 1;
      cout << "c: "<< c<< endl;
      labels[i] = c;
      growCluster(database, labels, i, c, epsilon, minPts);
    }
  }
  cout << "LABELS @ 1: " << labels[1] <<"LABELS @ 10: " << labels[10] << "!"<< endl;
  return labels;
}
