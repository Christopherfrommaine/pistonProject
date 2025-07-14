use std::{collections::BTreeMap, fmt::write};

#[derive(Clone, PartialEq)]
pub struct State {
    pub pistons: BTreeMap<i32, char>,
    pub observers: BTreeMap<i32, char>,
    pub moves: Vec<Move>,
    pub original: (String, String, Option<i32>),
}

#[derive(Clone, PartialEq)]
pub enum Move {
    Power(i32),
    Observer(i32),
    Custom(String),
    State(State),
}

impl std::fmt::Debug for Move {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Move::Power(i)   => write!(f, "{}", i),
            Move::Observer(i)   => write!(f, "({},)", i),
            Move::Custom(s)   => write!(f, "{}", s),
            Move::State(s) => write!(f, "{}", s), // assumes State: Display
        }
    }
}
impl std::fmt::Debug for State {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.basic_repr_with_f())
    }
}


impl State {
    pub fn new(piston_state: &str, observer_state: &str, zero_offset: Option<i32>) -> Self {
        let original = (piston_state.to_string(), observer_state.to_string(), zero_offset);
        
        // compute zero_offset if needed
        let mut zo = zero_offset;
        if zo.is_none() {
            for (i, c) in piston_state.chars().enumerate() {
                if c=='f' || c.is_uppercase() {
                    zo = Some(-(i as i32));
                    break;
                }
            }
        }
        let zero = zo.unwrap_or(0);
        let mut pistons = BTreeMap::new();
        for (i, c) in piston_state.chars().enumerate() {
            let key = i as i32 + zero;
            let val = if c=='f' { ' ' } else { c.to_ascii_lowercase() };
            pistons.insert(key, val);
        }
        let top = *pistons.keys().max().unwrap();
        pistons.insert(top+1, ' ');
        pistons.insert(top+2, ' ');

        let mut observers = BTreeMap::new();
        for (i, c) in observer_state.chars().enumerate() {
            observers.insert(-3 - (i as i32), c);
        }

        State { pistons, observers, moves: Vec::new(), original }
    }

    pub fn basic_repr(&self) -> String {
        self.pistons.values().collect()
    }

    pub fn basic_repr_with_f(&self) -> String {
        let mut map = self.pistons.clone();
        let ch = map.get(&0).cloned().unwrap_or(' ');
        map.insert(0, if ch==' ' {'f'} else { ch.to_ascii_uppercase() });
        map.values().collect()
    }

    pub fn full_repr(&self) -> String {
        let pist = self.pistons.values().collect::<String>();
        let pad = 100;
        let obs_keys = self.observers.keys().copied().collect::<Vec<_>>();
        let shift = obs_keys.iter().min().unwrap() - self.pistons.keys().min().unwrap();
        let mut line2 = " ".repeat(shift as usize);
        let obs_str: String = self.observers.values().rev().collect();
        line2.push_str(&obs_str);
        line2.push_str("  f\n");
        format!("{}{}{}\n", pist, " ".repeat(pad), line2)
    }
}

impl std::fmt::Display for State {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        if self.moves.last() == Some(&Move::Power(-1)) {
            write!(f, "-----")
        } else {
            write!(f, "{}", self.basic_repr_with_f())
        }
    }
}

impl State {
    pub fn original_state(&self) -> State {
        let (ps, os, zo) = &self.original;
        State::new(ps, os, *zo)
    }

    pub fn apply_move(&mut self, mv: Move) -> bool {
        self.moves.push(mv.clone());
        match mv {
            Move::Power(v) => {
                if v == 8*9 {return true;}
                if !(v <= -2) {return false;}
                self.apply_power_piston(v);
            },
            Move::Observer(observer) => {
                if *self.observers.get(&observer).unwrap() == 'o' {
                    if *self.pistons.get(&observer).unwrap() != ' ' {return false;}

                    self.observers.insert(observer, ' ');
                    self.pistons.insert(observer, 'o');

                    self.apply_power_piston(observer + 1)
                } else {
                    if *self.pistons.get(&observer).unwrap() != 'o' {return false;}

                    self.observers.insert(observer, 'o');
                    self.pistons.insert(observer, ' ');
                }
            }
            Move::State(s) => {
                self.pistons = s.pistons;
                self.observers = s.observers;
            }
            Move::Custom(_) => {}
        }
        return true;
    }

    pub fn apply_move_with_quasi(&mut self, mv: Move) -> bool {
        self.moves.push(mv.clone());
        match mv {
            Move::Power(v) => {
                if v == 8*9 {return true;}
                if !(v <= -2) {return false;}
                if *self.pistons.get(&v).unwrap() == ' ' && *self.pistons.get(&(v - 1)).unwrap() == 'p' {
                    self.apply_power_piston(v - 1);
                } else {
                    self.apply_power_piston(v);
                }
            },
            Move::Observer(observer) => {
                if *self.observers.get(&observer).unwrap() == 'o' {
                    if *self.pistons.get(&observer).unwrap() != ' ' {return false;}

                    self.observers.insert(observer, ' ');
                    self.pistons.insert(observer, 'o');

                    self.apply_power_piston(observer + 1)
                } else {
                    if *self.pistons.get(&observer).unwrap() != 'o' {return false;}

                    self.observers.insert(observer, 'o');
                    self.pistons.insert(observer, ' ');
                }
            }
            Move::State(s) => {
                self.pistons = s.pistons;
                self.observers = s.observers;
            }
            Move::Custom(_) => {}
        }
        return true;
    }

    fn apply_power_piston(&mut self, pos: i32) {
        if self.pistons.get(&pos)==Some(&'p') {
            if self.pistons.get(&(pos+1))==Some(&' ') {
                let a = self.pistons[&(pos+1)];
                let b = self.pistons[&(pos+2)];
                self.pistons.insert(pos+1, b);
                self.pistons.insert(pos+2, a);
                return;
            }
            let mut max_block = pos;
            for b in (pos+1)..=(pos+12) {
                if self.pistons[&b]==' ' {
                    max_block = b-1;
                    break;
                }
            }
            if max_block==pos { return; }
            let mut to_update = Vec::new();
            if self.pistons[&(pos+1)]=='o' {
                to_update.push(pos+1);
            }
            for b in (pos+1..=max_block).rev() {
                let c = self.pistons[&b];
                self.pistons.insert(b+1, c);
                if c=='o' { to_update.push(b+1); }
            }
            self.pistons.insert(pos+1, ' ');
            for u in to_update {
                if self.pistons.get(&(u+1))==Some(&'p') {
                    self.apply_power_piston(u+1);
                    break;
                }
            }
        }
    }

    pub fn apply_moves(&mut self, lst: &[Move]) -> bool{
        for m in lst {
            if !self.apply_move(m.clone()) {
                return false;
            }
        }
        return true;
    }
}



pub fn check_apply_corrections(moves: &Vec<Move>, state: State) -> bool {
    

    let mut o = Vec::new();
    for m in moves.iter() {
        match m {
            Move::Observer(observer) => {
                if *observer != -3 {continue;}
                
                for i in (*observer)..-2 {
                    if *state.pistons.get(&i).unwrap() == ' ' || i == *observer {
                        o.push(Move::Observer(i));
                        if *state.pistons.get(&(i + 1)).unwrap() == ' ' {
                            break;
                        }
                    }
                    else {
                        o.push(Move::Observer(i));
                        break
                    }
                }
            },
            Move::Power(m) => {
                if *m == 8 * 9 {
                    o.push(Move::Power(*m));
                    continue;
                }

                if *m >= -6 || m % 2 == 0 {
                    o.push(Move::Power(*m));
                } else {
                    if *state.pistons.get(&(m + 1)).unwrap() == ' ' {
                        o.push(Move::Power(m + 1));
                    } else {
                        o.push(Move::Power(m - 1));
                    }
                }
            },
            _ => {}
        }
    }

    let mut odoor = state.original_state();
    for m in o {
        let res = odoor.apply_move_with_quasi(m);
        if !res {
            return false;
        }
    }

    return true;
}