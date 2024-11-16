use anyhow::Result;
use plonky2::field::types::Field;
use plonky2::iop::witness::{PartialWitness, WitnessWrite};
use plonky2::plonk::circuit_builder::CircuitBuilder;
use plonky2::plonk::circuit_data::CircuitConfig;
use plonky2::plonk::config::{GenericConfig, PoseidonGoldilocksConfig};
use serde::{Deserialize, Serialize};
use serde_json;
use std::fs::{self, File};
use std::io::Read;
use std::io::Write;
use std::time::{SystemTime, UNIX_EPOCH};

// JSON data structure
#[derive(Serialize, Deserialize, Debug)] // Added Debug trait to allow printing of structs
struct CropConfig {
    vector: Vec<u32>,
    crop_segments: Vec<CropParams>,
}

#[derive(Serialize, Deserialize, Debug)] // Added Debug trait to allow printing of structs
struct CropParams {
    start_index: usize,
    crop_length: usize,
}

fn print_time_since(last: u128, tag: &str) -> u128 {
    let now = SystemTime::now();
    let now_epoc = now.duration_since(UNIX_EPOCH).expect("Time went backwards");
    let now = now_epoc.as_millis();
    println!(
        "{:?} - time since last check: {:?}",
        tag,
        (now - last) as f32 / 60000.0
    );
    return now;
}

fn main() -> Result<()> {
    const D: usize = 2;
    type C = PoseidonGoldilocksConfig;
    type F = <C as GenericConfig<D>>::F;

    // Read configuration from JSON file
    let mut file = File::open("video_process.json")?;
    let mut json_str = String::new();
    file.read_to_string(&mut json_str)?;
    let crop_config: CropConfig = serde_json::from_str(&json_str)?;

    let w_r_vals = crop_config.vector;
    let crop_segments = crop_config.crop_segments;

    // Validate crop parameters
    for segment in &crop_segments {
        if segment.start_index >= w_r_vals.len()
            || segment.start_index + segment.crop_length > w_r_vals.len()
        {
            return Err(anyhow::anyhow!(
                "Invalid crop range for segment: {:?}",
                segment
            ));
        }
    }

    // Extract all the cropped segments
    let mut cropped_values = Vec::new();
    for segment in &crop_segments {
        let start_index = segment.start_index;
        let crop_length = segment.crop_length;
        cropped_values.extend(&w_r_vals[start_index..start_index + crop_length]);
    }

    // Timing setup
    let start = SystemTime::now();
    let start_epoch = start
        .duration_since(UNIX_EPOCH)
        .expect("Time went backwards");
    let start = start_epoch.as_millis();
    let mut last = start;

    last = print_time_since(last, "values generated");

    let mut config = CircuitConfig::standard_recursion_config();
    config.zero_knowledge = true;
    let mut builder = CircuitBuilder::<F, D>::new(config);

    let mut pw = PartialWitness::new();

    let mut w_r_targets = Vec::new();

    // Dynamically create targets for cropped segments
    for _ in 0..cropped_values.len() {
        let r = builder.add_virtual_target();
        w_r_targets.push(r);
        builder.register_public_input(r);
    }

    let data = builder.build::<C>();
    last = print_time_since(last, "setup done");

    // Set values for the cropped targets
    for (i, &val) in cropped_values.iter().enumerate() {
        pw.set_target(w_r_targets[i], F::from_canonical_u32(val));
    }

    // Generate proof
    let proof = data.prove(pw)?;
    let compressed_proof = data.compress(proof)?;
    last = print_time_since(last, "proof done");

    // Save proof to file, overwriting if it already exists
    let proof_file_path = "proof.json";
    if fs::metadata(proof_file_path).is_ok() {
        println!("File '{}' exists and will be overwritten.", proof_file_path);
    }
    let mut proof_file = File::create(proof_file_path)?;
    proof_file.write_all(serde_json::to_string(&compressed_proof)?.as_bytes())?;

    // Export verification key and save to file, overwriting if it already exists
    let vk_file_path = "verification_key.json";
    if fs::metadata(vk_file_path).is_ok() {
        println!("File '{}' exists and will be overwritten.", vk_file_path);
    }
    let verifier_only = &data.verifier_only;
    let common = &data.common;

    let vk = (verifier_only, common);
    let mut vk_file = File::create(vk_file_path)?;
    vk_file.write_all(serde_json::to_string(&vk)?.as_bytes())?;

    println!("Proof and Verification Key successfully exported.");

    Ok(())
}
