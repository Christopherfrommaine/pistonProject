use std::time::Duration;

mod state;
mod simplify;
use state::*;

fn main() {
    // 1. Read the file
    let data = std::fs::read_to_string("src/input.txt").unwrap();

    // 2–4. Split, parse, unwrap, collect
    let moves: Vec<Move> = data
        .split_whitespace()
        .map(|tok| {
            // If it’s of the form "(<number>,)"
            if let Some(inner) = tok
                .strip_prefix('(')
                .and_then(|s| s.strip_suffix(",)"))
            {
                let i: i32 = inner.parse().unwrap();
                Move::Observer(i)
            } else {
                // Otherwise treat as a plain integer
                let i: i32 = tok.parse().unwrap();
                Move::Power(i)
            }
        })
        .collect();

    let mut s = State::new("pppppppppppppppppppppppppp  f         b  ", "ooooo", None);
    println!("{}", s.apply_moves(&moves));

    let simped = moves;
    // let simped = simplify::repeat_simplification(simped, &s.original_state(), simplify::thousand_at_a_time_par, true, Duration::from_secs(25));
    // let simped = simplify::repeat_simplification(simped, &s.original_state(), simplify::hundred_at_a_time_par, true, Duration::from_secs(15));
    // let simped = simplify::repeat_simplification(simped, &s.original_state(), simplify::five_at_a_time_par, true, Duration::from_secs(10));
    let simped = simplify::repeat_simplification(simped, &s.original_state(), simplify::one_at_a_time_par, true, Duration::from_secs(10));

    std::fs::write("src/output.txt", format!("{:?}", simped)).unwrap();

}
