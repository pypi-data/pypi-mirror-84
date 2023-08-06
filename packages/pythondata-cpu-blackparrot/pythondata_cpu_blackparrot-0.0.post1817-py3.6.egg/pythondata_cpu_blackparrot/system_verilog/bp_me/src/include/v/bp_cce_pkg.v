/**
 *
 * Name:
 *   bp_cce_pkg.v
 *
 * Description:
 *
 */

package bp_cce_pkg;

  import bp_common_pkg::*;

  `include "bp_me_cce_mem_if.vh"
  `include "bp_cce_inst.vh"

  `define bp_cce_mode_bits $bits(bp_cce_mode_e)

  // Miss Status Handling Register Struct
  // This struct tracks the information required to process an LCE request
  `define declare_bp_cce_mshr_s(lce_id_width_mp, lce_assoc_mp, paddr_width_mp) \
  typedef struct packed                                                   \
  {                                                                       \
    logic [lce_id_width_mp-1:0]                   lce_id;                 \
    logic [paddr_width_mp-1:0]                    paddr;                  \
    logic [`BSG_SAFE_CLOG2(lce_assoc_mp)-1:0]     way_id;                 \
    logic [paddr_width_mp-1:0]                    lru_paddr;              \
    logic [`BSG_SAFE_CLOG2(lce_assoc_mp)-1:0]     lru_way_id;             \
    logic [lce_id_width_mp-1:0]                   tr_lce_id;              \
    logic [`BSG_SAFE_CLOG2(lce_assoc_mp)-1:0]     tr_way_id;              \
    bp_coh_states_e                               next_coh_state;         \
    logic [`bp_cce_inst_num_flags-1:0]            flags;                  \
    bp_lce_cce_uc_req_size_e                      uc_req_size;            \
  } bp_cce_mshr_s

  `define bp_cce_mshr_width(lce_id_width_mp, lce_assoc_mp, paddr_width_mp) \
    ((2*lce_id_width_mp)+(3*`BSG_SAFE_CLOG2(lce_assoc_mp))+(2*paddr_width_mp) \
     +`bp_coh_bits+`bp_cce_inst_num_flags+$bits(bp_lce_cce_uc_req_size_e))

  // MSHR width for BP is:
  // 2*LOG(num_lce) + (9 + 78 + 3 + 15 + 2) = 2*LOG(num_lce) + 107

  `define declare_bp_cce_dir_entry_s(tag_width_mp) \
  typedef struct packed                            \
  {                                                \
    logic [tag_width_mp-1:0] tag;                  \
    bp_coh_states_e          state;                \
  } dir_entry_s                                    \


endpackage : bp_cce_pkg
