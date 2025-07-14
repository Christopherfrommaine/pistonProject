use std::time::{Duration, Instant};
use crate::state::{Move, State, check_apply_corrections};

/// Repeatedly apply `simp_func` to `moves` until it stops changing or timeout.
pub fn repeat_simplification<F>(
    mut moves: Vec<Move>,
    original: &State,
    simp_func: F,
    prnt: bool,
    time_limit: Duration,
) -> Vec<Move>
where
    F: Fn(&[Move], &State) -> Vec<Move>,
{
    let final_state = {
        let mut s = original.clone();
        s.apply_moves(&moves);
        s
    };
    let start = Instant::now();
    let mut old_moves: Vec<Move>;

    while start.elapsed() < time_limit {
        if prnt {
            println!("step, {}", moves.len());
        }
        old_moves = moves.clone();
        let candidate = simp_func(&old_moves, original);

        // verify equivalence
        let mut check = original.clone();
        if !check.apply_moves(&candidate) {
            return old_moves;
        }

        if !check_apply_corrections(&candidate, original.clone()) {
            return old_moves;
        }
    
        if check.full_repr() != final_state.full_repr() {
            return old_moves;
        }

        if candidate == old_moves {
            break;
        }
        moves = candidate;
    }

    if prnt {
        println!();
    }
    moves
}

/// Try removing one integer-type move at a time.
pub fn one_at_a_time(moves: &[Move], original: &State) -> Vec<Move> {
    let mut final_state = original.clone();
    final_state.apply_moves(moves);

    for i in 0..moves.len() {
        // only consider integer moves
        if let Move::Power(_) = moves[i] {
            let mut new_moves = moves.to_vec();
            new_moves.remove(i);

            let mut check = original.clone();
            if check.apply_moves(&new_moves) {
                if check.full_repr() == final_state.full_repr() {
                    return new_moves;
                }
            }
        }
    }
    moves.to_vec()
}

use rayon::prelude::*;

/// Try removing one integer-type move at a time.
pub fn one_at_a_time_par(moves: &[Move], original: &State) -> Vec<Move> {
    let mut final_state = original.clone();
    final_state.apply_moves(moves);

    let ind = (0..moves.len()).into_par_iter().find_first(|i| {
        // only consider integer moves
        if let Move::Power(_) = moves[*i] {
            let mut new_moves = moves.to_vec();
            new_moves.remove(*i);

            let mut check = original.clone();
            return check.apply_moves(&new_moves) && check.full_repr() == final_state.full_repr();
        } else if let Move::Observer(_) = moves[*i] {
            let mut new_moves = moves.to_vec();
            new_moves.remove(*i);

            let mut check = original.clone();
            return check.apply_moves(&new_moves) && check.full_repr() == final_state.full_repr() && check_apply_corrections(&new_moves, original.clone());
        } else {
            return false;
        }
    });

    if let Some(i) = ind {
        let mut new_moves = moves.to_vec();
        new_moves.remove(i);
        new_moves
    } else {
        moves.to_vec()
    }

    
}

/// Try removing n integers-type move at a time.
pub fn five_at_a_time_par(moves: &[Move], original: &State) -> Vec<Move> {
    let mut final_state = original.clone();
    final_state.apply_moves(moves);

    let ind = (0..(moves.len()-5)).into_par_iter().find_first(|i| {
        // only consider integer moves
        
        let mut new_moves = moves.to_vec();
        new_moves.remove(*i);
        new_moves.remove(*i);
        new_moves.remove(*i);
        new_moves.remove(*i);
        new_moves.remove(*i);

        if !moves[*i..(*i+5)].iter().all(|m| matches!(m, Move::Power(_) | Move::Observer(_))) {return false;}

        let mut check = original.clone();
        return check.apply_moves(&new_moves) && check.full_repr() == final_state.full_repr() && check_apply_corrections(&new_moves, original.clone());
        
    });

    if let Some(i) = ind {
        let mut new_moves = moves.to_vec();
        new_moves.remove(i);
        new_moves.remove(i);
        new_moves.remove(i);
        new_moves.remove(i);
        new_moves.remove(i);
        new_moves
    } else {
        moves.to_vec()
    }

    
}

/// Try removing n integers-type move at a time.
pub fn hundred_at_a_time_par(moves: &[Move], original: &State) -> Vec<Move> {
    if moves.len() < 100 {return moves.to_vec();}

    let mut final_state = original.clone();
    final_state.apply_moves(moves);

    let ind = (0..(moves.len()-100)).into_par_iter().find_first(|i| {
        // only consider integer moves
        if !moves[*i..(*i+100)].iter().all(|m| matches!(m, Move::Power(_) | Move::Observer(_))) {return false;}

        let mut new_moves = moves[..*i].to_vec();
        new_moves.extend_from_slice(&moves[(*i + 100)..]);

        let mut check = original.clone();
        return check.apply_moves(&new_moves) && check.full_repr() == final_state.full_repr() && check_apply_corrections(&new_moves, original.clone());
    
    });

    if let Some(i) = ind {
        let mut new_moves = moves[..i].to_vec();
        new_moves.extend_from_slice(&moves[(i + 100)..]);
        new_moves
    } else {
        moves.to_vec()
    }

    
}

/// Try removing n integers-type move at a time.
pub fn thousand_at_a_time_par(moves: &[Move], original: &State) -> Vec<Move> {
    if moves.len() < 1000 {return moves.to_vec();}

    let mut final_state = original.clone();
    final_state.apply_moves(moves);

    let ind = (0..(moves.len()-1000)).into_par_iter().find_first(|i| {
        // only consider integer moves
        if !moves[*i..(*i+1000)].iter().all(|m| matches!(m, Move::Power(_) | Move::Observer(_))) {return false;}
        
        let mut new_moves = moves[..*i].to_vec();
        new_moves.extend_from_slice(&moves[(*i + 1000)..]);

        let mut check = original.clone();
        return check.apply_moves(&new_moves) && check.full_repr() == final_state.full_repr() && check_apply_corrections(&new_moves, original.clone());
        
    });

    if let Some(i) = ind {
        let mut new_moves = moves[..i].to_vec();
        new_moves.extend_from_slice(&moves[(i + 1000)..]);
        new_moves
    } else {
        moves.to_vec()
    }

    
}

/// Context-aware two-int replacement simplification.
pub fn context_aware_replacement_simplification(
    moves: &[Move],
    original: &State,
) -> Vec<Move> {
    let mut state = original.clone();
    let mut output = Vec::with_capacity(moves.len());
    let mut mi = 0;

    while mi < moves.len() {
        // look ahead
        if mi + 1 < moves.len() {
            if let (Move::Power(a), Move::Power(b)) = (&moves[mi], &moves[mi+1]) {
                if *b < *a {
                    // check that pistons are all 'p' in [b..=a]
                    let range_ok = (*b..=*a).all(|i| *state.pistons.get(&i).unwrap() == 'p');
                    if range_ok {
                        output.push(Move::Power(*b));
                        mi += 2;
                        continue;
                    }
                }
            }
        }
        // otherwise, keep this move and advance
        output.push(moves[mi].clone());
        state.apply_move(moves[mi].clone());
        mi += 1;
    }

    output
}
