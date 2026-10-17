<script setup lang="ts">
import { computed } from 'vue';
import type { ChildGender } from '../../composables/useChildProfile';

const props = withDefaults(
  defineProps<{
    ageMonths?: number;
    gender?: ChildGender;
    size?: number | string;
  }>(),
  {
    ageMonths: 14,
    gender: 'boy',
    size: 44,
  }
);

// Map months to development stage: infant (0-8m), toddler (9-23m), preschool (24-60m)
const stage = computed<'infant' | 'toddler' | 'preschool'>(() => {
  const age = Number(props.ageMonths) || 0;
  if (age <= 8) return 'infant';
  if (age <= 23) return 'toddler';
  return 'preschool';
});

// Unique ID for SVG clipping paths
const clipId = `avatar-clip-${Math.random().toString(36).substring(2, 9)}`;

const avatarLabel = computed(() => {
  const genderText = props.gender === 'girl' ? 'Perempuan' : 'Laki-laki';
  const stageText =
    stage.value === 'infant' ? 'Bayi' : stage.value === 'toddler' ? 'Batita' : 'Balita';
  return `Ilustrasi ${stageText} ${genderText} (${props.ageMonths} bulan)`;
});
</script>

<template>
  <svg
    :width="size"
    :height="size"
    viewBox="0 0 100 100"
    role="img"
    :aria-label="avatarLabel"
    style="display: inline-block; vertical-align: middle; flex-shrink: 0;"
  >
    <defs>
      <clipPath :id="clipId">
        <circle cx="50" cy="50" r="47" />
      </clipPath>
    </defs>

    <!-- Base Frame Background -->
    <circle
      cx="50"
      cy="50"
      r="47"
      fill="var(--paper-2, #F8F4EE)"
      stroke="var(--line-strong, #D8CEBE)"
      stroke-width="2.5"
    />

    <!-- Clipped Avatar Content -->
    <g :clip-path="`url(#${clipId})`">
      <!-- ======================================================== -->
      <!-- VARIANT 1: INFANT BOY (0 - 8 BULAN)                      -->
      <!-- ======================================================== -->
      <g v-if="stage === 'infant' && gender === 'boy'">
        <!-- Infant Body & Swaddle/Bib -->
        <path d="M 20 100 C 20 78, 80 78, 80 100 Z" fill="#6B8055" />
        <path d="M 33 74 C 36 88, 64 88, 67 74 C 60 76, 40 76, 33 74 Z" fill="#F8F4EE" />
        
        <!-- Ears -->
        <circle cx="23" cy="52" r="6" fill="#FCD5B5" />
        <circle cx="23" cy="52" r="3.5" fill="#F5B895" />
        <circle cx="77" cy="52" r="6" fill="#FCD5B5" />
        <circle cx="77" cy="52" r="3.5" fill="#F5B895" />

        <!-- Round Baby Head -->
        <circle cx="50" cy="52" r="27" fill="#FCD5B5" />

        <!-- Baby Hair Tuft / Swirl on top -->
        <path d="M 50 25 C 54 15, 46 11, 43 14 C 40 18, 48 20, 48 25 Z" fill="#3C2415" />
        <path d="M 52 25 C 56 18, 51 14, 48 16" stroke="#3C2415" stroke-width="2" stroke-linecap="round" fill="none" />

        <!-- Rosy Cheeks -->
        <circle cx="35" cy="57" r="6" fill="#F87171" opacity="0.32" />
        <circle cx="65" cy="57" r="6" fill="#F87171" opacity="0.32" />

        <!-- Big Sparkling Eyes -->
        <ellipse cx="38" cy="49" rx="3.8" ry="4.8" fill="#251B14" />
        <circle cx="39.5" cy="47.5" r="1.5" fill="#FFFFFF" />
        <ellipse cx="62" cy="49" rx="3.8" ry="4.8" fill="#251B14" />
        <circle cx="63.5" cy="47.5" r="1.5" fill="#FFFFFF" />

        <!-- Tiny Cute Nose & Baby Smile -->
        <circle cx="50" cy="54" r="1.2" fill="#D39775" />
        <path d="M 46 59 Q 50 64 54 59" stroke="#9A382A" stroke-width="2.2" stroke-linecap="round" fill="#E26D5C" />
      </g>

      <!-- ======================================================== -->
      <!-- VARIANT 2: INFANT GIRL (0 - 8 BULAN)                     -->
      <!-- ======================================================== -->
      <g v-else-if="stage === 'infant' && gender === 'girl'">
        <!-- Infant Body & Bib -->
        <path d="M 20 100 C 20 78, 80 78, 80 100 Z" fill="#D97757" />
        <path d="M 33 74 C 36 88, 64 88, 67 74 C 60 76, 40 76, 33 74 Z" fill="#F8F4EE" />

        <!-- Ears -->
        <circle cx="23" cy="52" r="6" fill="#FCD5B5" />
        <circle cx="23" cy="52" r="3.5" fill="#F5B895" />
        <circle cx="77" cy="52" r="6" fill="#FCD5B5" />
        <circle cx="77" cy="52" r="3.5" fill="#F5B895" />

        <!-- Round Baby Head -->
        <circle cx="50" cy="52" r="27" fill="#FCD5B5" />

        <!-- Soft Baby Curls -->
        <circle cx="26" cy="40" r="4.5" fill="#3C2415" />
        <circle cx="74" cy="40" r="4.5" fill="#3C2415" />

        <!-- Floral Headband -->
        <path d="M 24 45 Q 50 35 76 45" stroke="#E26D5C" stroke-width="3.5" stroke-linecap="round" fill="none" />
        <!-- Headband Flower -->
        <circle cx="68" cy="38" r="4.5" fill="#F43F5E" />
        <circle cx="68" cy="38" r="2" fill="#FDE047" />

        <!-- Rosy Cheeks -->
        <circle cx="35" cy="57" r="6" fill="#F87171" opacity="0.38" />
        <circle cx="65" cy="57" r="6" fill="#F87171" opacity="0.38" />

        <!-- Big Sparkling Eyes with Cute Lashes -->
        <ellipse cx="38" cy="49" rx="3.8" ry="4.8" fill="#251B14" />
        <circle cx="39.5" cy="47.5" r="1.5" fill="#FFFFFF" />
        <path d="M 34 46 L 31 44" stroke="#251B14" stroke-width="1.6" stroke-linecap="round" />
        
        <ellipse cx="62" cy="49" rx="3.8" ry="4.8" fill="#251B14" />
        <circle cx="63.5" cy="47.5" r="1.5" fill="#FFFFFF" />
        <path d="M 66 46 L 69 44" stroke="#251B14" stroke-width="1.6" stroke-linecap="round" />

        <!-- Sweet Baby Smile -->
        <circle cx="50" cy="54" r="1.2" fill="#D39775" />
        <path d="M 46 59 Q 50 64 54 59" stroke="#9A382A" stroke-width="2.2" stroke-linecap="round" fill="#E26D5C" />
      </g>

      <!-- ======================================================== -->
      <!-- VARIANT 3: TODDLER BOY (9 - 23 BULAN - e.g. BIMA)        -->
      <!-- ======================================================== -->
      <g v-else-if="stage === 'toddler' && gender === 'boy'">
        <!-- Shirt in Warm Olive -->
        <path d="M 16 100 C 16 75, 84 75, 84 100 Z" fill="#5A7142" />
        <!-- Rounded Collar -->
        <path d="M 38 74 Q 50 82 62 74 Q 50 78 38 74 Z" fill="#E8DEC9" />

        <!-- Ears -->
        <circle cx="24" cy="49" r="6.5" fill="#FCD5B5" />
        <circle cx="24" cy="49" r="4" fill="#F5B895" />
        <circle cx="76" cy="49" r="6.5" fill="#FCD5B5" />
        <circle cx="76" cy="49" r="4" fill="#F5B895" />

        <!-- Head -->
        <circle cx="50" cy="49" r="25" fill="#FCD5B5" />

        <!-- Boy Toddler Haircut (Back + Top + Bangs) -->
        <path
          d="M 23 48 C 21 28, 36 17, 50 17 C 64 17, 79 28, 77 48 C 72 37, 63 32, 53 33 C 43 35, 33 33, 23 48 Z"
          fill="#3C2415"
        />
        <!-- Front Bang Tufts -->
        <path d="M 33 33 Q 41 39 49 34 Q 40 30 33 33 Z" fill="#3C2415" />
        <path d="M 46 34 Q 56 39 63 33 Q 54 30 46 34 Z" fill="#3C2415" />

        <!-- Rosy Cheeks -->
        <circle cx="36" cy="56" r="5.5" fill="#F87171" opacity="0.32" />
        <circle cx="64" cy="56" r="5.5" fill="#F87171" opacity="0.32" />

        <!-- Toddler Cheerful Eyes -->
        <ellipse cx="39" cy="48" rx="3.6" ry="4.5" fill="#251B14" />
        <circle cx="40.3" cy="46.7" r="1.4" fill="#FFFFFF" />
        <ellipse cx="61" cy="48" rx="3.6" ry="4.5" fill="#251B14" />
        <circle cx="62.3" cy="46.7" r="1.4" fill="#FFFFFF" />

        <!-- Toddler Happy Smile -->
        <circle cx="50" cy="53" r="1.2" fill="#D39775" />
        <path d="M 44 57 Q 50 65 56 57" stroke="#9A382A" stroke-width="2.2" stroke-linecap="round" fill="#E26D5C" />
      </g>

      <!-- ======================================================== -->
      <!-- VARIANT 4: TODDLER GIRL (9 - 23 BULAN)                   -->
      <!-- ======================================================== -->
      <g v-else-if="stage === 'toddler' && gender === 'girl'">
        <!-- Side Bun Hair (Behind Ears) -->
        <circle cx="23" cy="32" r="9.5" fill="#3C2415" />
        <ellipse cx="29" cy="38" rx="3.5" ry="2.2" fill="#D97757" />
        <circle cx="77" cy="32" r="9.5" fill="#3C2415" />
        <ellipse cx="71" cy="38" rx="3.5" ry="2.2" fill="#D97757" />

        <!-- Blouse in Warm Terracotta -->
        <path d="M 16 100 C 16 75, 84 75, 84 100 Z" fill="#C25E3E" />
        <path d="M 37 74 Q 50 82 63 74 Q 50 78 37 74 Z" fill="#F8F4EE" />

        <!-- Ears -->
        <circle cx="24" cy="49" r="6.5" fill="#FCD5B5" />
        <circle cx="24" cy="49" r="4" fill="#F5B895" />
        <circle cx="76" cy="49" r="6.5" fill="#FCD5B5" />
        <circle cx="76" cy="49" r="4" fill="#F5B895" />

        <!-- Head -->
        <circle cx="50" cy="49" r="25" fill="#FCD5B5" />

        <!-- Front Bangs / Hair Cap -->
        <path
          d="M 24 46 C 23 28, 36 19, 50 19 C 64 19, 77 28, 76 46 C 70 36, 61 33, 50 33 C 39 33, 30 36, 24 46 Z"
          fill="#3C2415"
        />

        <!-- Rosy Cheeks -->
        <circle cx="36" cy="56" r="6" fill="#F87171" opacity="0.38" />
        <circle cx="64" cy="56" r="6" fill="#F87171" opacity="0.38" />

        <!-- Shiny Eyes + Little Lashes -->
        <ellipse cx="39" cy="48" rx="3.6" ry="4.5" fill="#251B14" />
        <circle cx="40.3" cy="46.7" r="1.4" fill="#FFFFFF" />
        <path d="M 35 45 L 32 43" stroke="#251B14" stroke-width="1.6" stroke-linecap="round" />

        <ellipse cx="61" cy="48" rx="3.6" ry="4.5" fill="#251B14" />
        <circle cx="62.3" cy="46.7" r="1.4" fill="#FFFFFF" />
        <path d="M 65 45 L 68 43" stroke="#251B14" stroke-width="1.6" stroke-linecap="round" />

        <!-- Sweet Toddler Smile -->
        <circle cx="50" cy="53" r="1.2" fill="#D39775" />
        <path d="M 44 57 Q 50 65 56 57" stroke="#9A382A" stroke-width="2.2" stroke-linecap="round" fill="#E26D5C" />
      </g>

      <!-- ======================================================== -->
      <!-- VARIANT 5: PRESCHOOL BOY (24 - 60 BULAN)                 -->
      <!-- ======================================================== -->
      <g v-else-if="stage === 'preschool' && gender === 'boy'">
        <!-- Polo Collar Shirt in Deep Forest Sage -->
        <path d="M 16 100 C 16 73, 84 73, 84 100 Z" fill="#445E32" />
        <!-- Polo Collar Wing & Placket -->
        <path d="M 36 73 L 45 81 L 50 76 L 55 81 L 64 73 Z" fill="#E8DEC9" />
        <circle cx="50" cy="85" r="1.3" fill="#E8DEC9" />

        <!-- Ears -->
        <circle cx="25" cy="47" r="6.5" fill="#FCD5B5" />
        <circle cx="25" cy="47" r="4" fill="#F5B895" />
        <circle cx="75" cy="47" r="6.5" fill="#FCD5B5" />
        <circle cx="75" cy="47" r="4" fill="#F5B895" />

        <!-- Head -->
        <circle cx="50" cy="47" r="24" fill="#FCD5B5" />

        <!-- Modern Cool Boy Cut (Side-swept bangs) -->
        <path
          d="M 24 45 C 23 25, 36 15, 52 15 C 68 15, 78 25, 76 45 C 72 32, 63 26, 48 26 C 35 26, 29 32, 24 45 Z"
          fill="#321D12"
        />
        <!-- Textured Bangs Sweeping Across -->
        <path d="M 30 26 Q 48 35 65 27 Q 50 20 30 26 Z" fill="#321D12" />

        <!-- Cheeks -->
        <circle cx="36" cy="54" r="5" fill="#F87171" opacity="0.28" />
        <circle cx="64" cy="54" r="5" fill="#F87171" opacity="0.28" />

        <!-- Bright Preschool Eyes -->
        <ellipse cx="39" cy="46" rx="3.5" ry="4.2" fill="#251B14" />
        <circle cx="40.3" cy="44.8" r="1.3" fill="#FFFFFF" />
        <ellipse cx="61" cy="46" rx="3.5" ry="4.2" fill="#251B14" />
        <circle cx="62.3" cy="44.8" r="1.3" fill="#FFFFFF" />

        <!-- Confident Smile -->
        <circle cx="50" cy="51" r="1.2" fill="#D39775" />
        <path d="M 43 55 Q 50 63 57 55" stroke="#9A382A" stroke-width="2.4" stroke-linecap="round" fill="#E26D5C" />
      </g>

      <!-- ======================================================== -->
      <!-- VARIANT 6: PRESCHOOL GIRL (24 - 60 BULAN - e.g. CINTA)   -->
      <!-- ======================================================== -->
      <g v-else>
        <!-- Hair behind (Bob length framing shoulders) -->
        <path
          d="M 22 45 C 19 66, 28 75, 32 75 L 68 75 C 72 75, 81 66, 78 45 C 77 24, 65 15, 50 15 C 35 15, 23 24, 22 45 Z"
          fill="#321D12"
        />

        <!-- Sweet Blouse in Warm Berry/Clay -->
        <path d="M 16 100 C 16 73, 84 73, 84 100 Z" fill="#B44B36" />
        <!-- Peter Pan Collar -->
        <path d="M 35 73 C 38 82, 48 81, 50 75 C 52 81, 62 82, 65 73 Z" fill="#F8F4EE" />

        <!-- Ears -->
        <circle cx="25" cy="47" r="6.5" fill="#FCD5B5" />
        <circle cx="25" cy="47" r="4" fill="#F5B895" />
        <circle cx="75" cy="47" r="6.5" fill="#FCD5B5" />
        <circle cx="75" cy="47" r="4" fill="#F5B895" />

        <!-- Face / Head -->
        <circle cx="50" cy="47" r="24" fill="#FCD5B5" />

        <!-- Bob Bangs & Headband -->
        <path d="M 26 40 C 33 29, 67 29, 74 40 C 67 33, 58 31, 50 31 C 42 31, 33 33, 26 40 Z" fill="#321D12" />
        
        <!-- Mustard/Gold Headband -->
        <path d="M 25 38 Q 50 24 75 38" stroke="#D97757" stroke-width="3.2" stroke-linecap="round" fill="none" />
        <circle cx="31" cy="33" r="3.5" fill="#FBBF24" />

        <!-- Cheeks -->
        <circle cx="36" cy="54" r="5.5" fill="#F87171" opacity="0.36" />
        <circle cx="64" cy="54" r="5.5" fill="#F87171" opacity="0.36" />

        <!-- Bright Friendly Eyes with Lashes -->
        <ellipse cx="39" cy="46" rx="3.5" ry="4.2" fill="#251B14" />
        <circle cx="40.3" cy="44.8" r="1.3" fill="#FFFFFF" />
        <path d="M 35 43 L 32 41" stroke="#251B14" stroke-width="1.6" stroke-linecap="round" />

        <ellipse cx="61" cy="46" rx="3.5" ry="4.2" fill="#251B14" />
        <circle cx="62.3" cy="44.8" r="1.3" fill="#FFFFFF" />
        <path d="M 65 43 L 68 41" stroke="#251B14" stroke-width="1.6" stroke-linecap="round" />

        <!-- Happy Smile -->
        <circle cx="50" cy="51" r="1.2" fill="#D39775" />
        <path d="M 43 55 Q 50 63 57 55" stroke="#9A382A" stroke-width="2.4" stroke-linecap="round" fill="#E26D5C" />
      </g>
    </g>
  </svg>
</template>
