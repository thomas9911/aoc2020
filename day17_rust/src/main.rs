use itertools;
use itertools::Itertools;
use std::collections::BTreeMap;
use std::fs::read_to_string;

type Index = Vec<isize>;

#[derive(Debug, Clone, PartialEq)]
pub enum Activated {
    Yes = 1,
    No = 0,
}

#[derive(Debug, Clone)]
pub struct Axes {
    axes: BTreeMap<usize, (isize, isize)>,
    dimensions: usize,
}

impl Axes {
    pub fn new(size: usize) -> Axes {
        let mut axes = BTreeMap::new();
        for i in 0..size {
            axes.insert(i, (0, 0));
        }

        Axes {
            axes,
            dimensions: size,
        }
    }

    pub fn expand(&mut self) {
        for (_, v) in self.axes.iter_mut() {
            // println!("{:?}", v);
            v.0 -= 1;
            v.1 += 1;
        }
    }

    pub fn max(&self, dimension: usize) -> isize {
        self.min_max(dimension).1
    }

    pub fn min(&self, dimension: usize) -> isize {
        self.min_max(dimension).0
    }

    pub fn min_max(&self, dimension: usize) -> &(isize, isize) {
        self.axes.get(&dimension).expect("invalid internal data")
    }

    pub fn get(&self, key: &usize) -> Option<&(isize, isize)> {
        self.axes.get(key)
    }

    pub fn update(&mut self, key: usize, min_max: (isize, isize)) {
        self.axes.insert(key, min_max);
    }

    pub fn iter(&self) -> AxesIter {
        AxesIter::new(self, self.dimensions)
    }
}

pub struct AxesIter {
    previous: Index,
    min: Index,
    max: Index,
}

impl AxesIter {
    fn new(data: &Axes, dimensions: usize) -> AxesIter {
        let mut first = Vec::with_capacity(dimensions);
        for i in 0..dimensions {
            let a = data.get(&i).expect("invalid internal data").0;
            if i == (dimensions - 1) {
                first.push(a - 1);
            } else {
                first.push(a);
            }
        }
        let max = Self::_get_max(&data, dimensions);
        let min = Self::_get_min(&data, dimensions);

        AxesIter {
            previous: first,
            max,
            min,
        }
    }

    fn _get_max(data: &Axes, dimensions: usize) -> Index {
        let mut max = Vec::with_capacity(dimensions);
        for i in 0..dimensions {
            let a = data.get(&i).expect("invalid internal data").1;
            max.push(a);
        }
        max
    }
    fn _get_min(data: &Axes, dimensions: usize) -> Index {
        let mut min = Vec::with_capacity(dimensions);
        for i in 0..dimensions {
            let a = data.get(&i).expect("invalid internal data").0;
            min.push(a);
        }
        min
    }
}

impl Iterator for AxesIter {
    type Item = Index;

    fn next(&mut self) -> Option<Self::Item> {
        if let Some(x) = next(&self.previous, &self.min, &self.max) {
            self.previous = x.clone();
            return Some(x);
        } else {
            return None;
        }
    }
}

fn next(previous: &Index, min: &Index, max: &Index) -> Option<Index> {
    if previous == max {
        return None;
    };

    let mut new = previous.clone();
    for i in (0..min.len()).rev() {
        if max[i] > previous[i] {
            new[i] += 1;
            break;
        } else {
            new[i] = min[i];
        }
    }
    Some(new)
}

#[derive(Debug)]
pub struct Board<S> {
    data: BTreeMap<Index, S>,
    axes: Axes,
}

impl<S> Board<S> {
    pub fn new(size: usize) -> Board<S> {
        Board {
            data: BTreeMap::new(),
            axes: Axes::new(size),
        }
    }

    pub fn get(&self, key: &Index) -> Option<&S> {
        self.data.get(key)
    }

    pub fn insert(&mut self, key: Index, value: S) -> Option<S> {
        for (d, index) in key.iter().enumerate() {
            if &self.axes.max(d) < index {
                let old_min = self.axes.min(d);
                self.axes.update(d, (old_min, *index));
            }

            if &self.axes.min(d) > index {
                let old_max = self.axes.max(d);
                self.axes.update(d, (*index, old_max));
            }
        }

        self.data.insert(key, value)
    }

    pub fn iter<'a>(&'a self) -> BoardIter<S> {
        BoardIter {
            data: &self.data,
            axes: self.axes.iter(),
        }
    }
}

impl Board<Activated> {
    pub fn load_text(&mut self, text: &str) {
        for (x, line) in text.split_ascii_whitespace().enumerate() {
            for (y, c) in line.chars().enumerate() {
                if c == '#' {
                    let mut point = Vec::with_capacity(self.axes.dimensions);
                    point.push(x as isize);
                    point.push(y as isize);
                    point.resize(self.axes.dimensions, 0);
                    self.insert(point, Activated::Yes);
                }
            }
        }
    }

    pub fn active(&self, key: &Index) -> bool {
        match self.get(key).unwrap_or(&Activated::No) {
            Activated::Yes => true,
            Activated::No => false,
        }
    }

    pub fn amount_active(&self) -> usize {
        self.data.values().len()
    }

    fn neighbours(key: &Index) -> Vec<Index> {
        let mut list = Vec::new();

        for i in itertools::repeat_n(-1..=1, key.len()).multi_cartesian_product() {
            let a: Index = key.iter().zip(i).map(|(a, b)| a + b).collect();
            if &a == key {
                continue;
            };

            list.push(a)
        }

        list
    }

    pub fn check_neighbours(&self, key: &Index) -> Activated {
        let mut active_neighbours = 0;
        for neighbour in Self::neighbours(&key) {
            if self.active(&neighbour) {
                active_neighbours += 1
            }
        }

        let active = self.active(key);

        // Rules

        if active && [2, 3].contains(&active_neighbours) {
            return Activated::Yes;
        }

        if active {
            return Activated::No;
        }

        if !active && (active_neighbours == 3) {
            return Activated::Yes;
        }

        Activated::No
    }

    pub fn next(&mut self) {
        self.axes.expand();

        let mut new_data = BTreeMap::new();

        for item in self.axes.iter() {
            match self.check_neighbours(&item) {
                Activated::Yes => {
                    new_data.insert(item, Activated::Yes);
                }
                Activated::No => ()
            }
        }

        self.data = new_data;

    }


}

pub struct BoardIter<'a, S> {
    data: &'a BTreeMap<Index, S>,
    axes: AxesIter,
}

impl<'a, V: std::fmt::Debug> Iterator for BoardIter<'a, V> {
    type Item = (Index, Option<&'a V>);

    fn next(&mut self) -> Option<Self::Item> {
        if let Some(index) = self.axes.next() {
            let x = self.data.get(&index);
            return Some((index, x));
        }

        None
    }
}

fn main() {
    let data = read_to_string("data.txt").expect("data file not found");

    const AMOUNT_DIMENSIONS: usize = 4;
    let mut board: Board<Activated> = Board::new(AMOUNT_DIMENSIONS);

    board.load_text(&data);

    println!("{:?}", board.amount_active());

    for _ in 0..6 {
        board.next()
    }

    println!("{:?}", board.amount_active());
}
