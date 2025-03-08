const Migrations = artifacts.require("Migrations");

module.exports = async function (deployer, network, accounts) {
  try {
    // Deploy the Migrations contract
    await deployer.deploy(Migrations);
    console.log("Migrations contract deployed successfully.");

    // Get the deployed instance of the Migrations contract
    const migrationsInstance = await Migrations.deployed();

    // Check the last completed migration
    const lastCompleted = await migrationsInstance.lastCompletedMigration();
    if (lastCompleted.toNumber() === 0) {
      // Set the initial completed migration to 1 if not already set
      await migrationsInstance.setCompleted(1);
      console.log("Initial migration marked as completed.");
    } else {
      console.log("Initial migration has already been completed.");
    }
  } catch (error) {
    console.error("Error during migration:", error);
    throw error; // Rethrow the error to stop the migration process
  }
};
