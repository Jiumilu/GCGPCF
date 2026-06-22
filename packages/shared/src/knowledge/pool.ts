export const KDS_POOL_CODES = [
  "order_pool",
  "logistics_pool",
  "capacity_pool",
  "finance_pool",
  "policy_pool",
  "equipment_pool",
  "data_pool",
  "energy_pool",
  "material_pool",
  "talent_pool",
  "scenario_pool",
] as const;

export type KdsPoolCode = (typeof KDS_POOL_CODES)[number];

export interface PoolBinding {
  id: string;
  tenantId: string;
  objectId: string;
  poolCode: KdsPoolCode;
  bindingReason?: string;
  bindingSource: "system" | "ai" | "user" | "policy" | "committee";
  createdBy: string;
  createdAt: string;
}

export interface KdsPoolDefinition {
  code: KdsPoolCode;
  label: string;
  description?: string;
  defaultObjectTypes?: string[];
}
