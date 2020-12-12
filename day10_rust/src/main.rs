use std::collections::{BTreeMap, BTreeSet};
use std::fs;

type Integer = u64;

#[derive(Debug)]
pub struct Graph {
    vertexes: BTreeSet<Integer>,
    edges: BTreeSet<(Integer, Integer)>,
    cached: BTreeMap<Integer, u128>,
}

const N: Integer = 3;

impl Graph {
    pub fn new() -> Graph {
        let mut vertexes = BTreeSet::new();
        vertexes.insert(0);
        Graph {
            vertexes,
            edges: BTreeSet::new(),
            cached: BTreeMap::new(),
        }
    }

    pub fn add_vertex(&mut self, vertex: Integer) {
        self.vertexes.insert(vertex);
        self.add_edges(vertex);
    }

    fn add_edges(&mut self, new_vertex: Integer) {
        let lower = new_vertex.saturating_sub(N);
        let upper = new_vertex + N;

        for index in lower..=upper {
            if index == new_vertex {
                continue;
            };

            if self.vertexes.contains(&index) {
                if new_vertex > index {
                    self.edges.insert((index, new_vertex));
                } else {
                    self.edges.insert((new_vertex, index));
                }
            }
        }
    }

    pub fn longest_path(&self) -> Vec<Integer> {
        return self.calc_longest_path(0, Vec::new());
    }

    fn calc_longest_path(&self, starting_point: Integer, path: Vec<Integer>) -> Vec<Integer> {
        for (a, b) in self.edges.iter().filter(|x| x.0 == starting_point) {
            let mut new_path = path;
            new_path.push(*a);
            return self.calc_longest_path(*b, new_path);
        }
        let mut new_path = path;
        new_path.push(starting_point);
        return new_path;
    }

    pub fn all_paths(&self) -> Vec<Vec<Integer>> {
        return self.calc_all_paths(0, Vec::new());
    }

    pub fn count_all_paths(&mut self) -> u128 {
        self.counting_all_paths_cacher(0)
    }

    fn calc_all_paths(
        &self,
        starting_point: Integer,
        paths: Vec<Vec<Integer>>,
    ) -> Vec<Vec<Integer>> {
        let mut the_paths = Vec::new();
        for (a, b) in self.edges.iter().filter(|x| x.0 == starting_point) {
            let length_paths = paths.len();
            let mut new_paths = paths.clone();
            if let (path_index, false) = length_paths.overflowing_sub(1) {
                new_paths[path_index].push(*a);
            } else {
                new_paths.push(vec![*a])
            };
            let p = self.calc_all_paths(*b, new_paths);

            for path in p {
                the_paths.push(path)
            }
        }

        if the_paths.len() > 0 {
            return the_paths;
        }
        let length_paths = paths.len();
        let mut new_paths = paths;
        new_paths[length_paths - 1].push(starting_point);
        return new_paths;
    }

    fn counting_all_paths_cacher(&mut self, starting_point: Integer) -> u128 {
        if let Some(from_cache) = self.cached.get(&starting_point) {
            return *from_cache;
        } else {
            let result = self.counting_all_paths(starting_point);
            self.cached.insert(starting_point, result);
            result
        }
    }

    fn counting_all_paths(&mut self, starting_point: Integer) -> u128 {
        let mut more = 0;
        let mut looped = false;
        for (_a, b) in self.edges.clone().iter().filter(|x| x.0 == starting_point) {
            looped = true;

            let new_counter = self.counting_all_paths_cacher(*b);
            more += new_counter;
        }

        if looped {
            return more;
        }

        return 1;
    }
}

fn main() {
    // println!("Hello, world!");

    let contents = fs::read_to_string("data.txt").expect("Unable to read file");
    let data = contents
        .split_ascii_whitespace()
        .map(|x| x.parse::<Integer>().unwrap());

    let mut g = Graph::new();
    for item in data {
        g.add_vertex(item)
    }
    // println!("{:?}", g.longest_path());
    // println!("{:?}", g.vertexes);

    // println!("{:?}", g)
    println!("{:?}", g.count_all_paths());
}
